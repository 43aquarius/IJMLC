#!/usr/bin/env python3
"""CIFAR extension: model, data loading and training for the cross-architecture
budget-matched comparison. Mirrors common.py (MLP pipeline) exactly except for
the model family and dataset; metric functions are imported from common.py so
that implementations are bit-identical across studies.

Determinism: same conventions as the MLP pipeline (torch.manual_seed(seed) at
model construction; data-order stream = torch.Generator seeded seed+1).
"""
import math
import os
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402  (metric implementations shared with v1/v2)
    nll, accuracy, brier, ece, ood_auroc, pairwise_jsd,
    fit_temperature, apply_temperature, log_probs_as_logits, TrainConfig,
)

torch.set_num_threads(int(os.environ.get("TORCH_THREADS", "2")))

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

DATA_PATH_CIFAR = paths.DATASETS_CIFAR
SPLIT_SEED_CIFAR = 20261012  # fixed, documented (new dataset -> new split seed)


# --------------------------------------------------------------------------- model

class SmallCNN(nn.Module):
    """3 conv blocks + FC head; ~34k parameters, no BN/dropout."""

    def __init__(self, seed: int):
        super().__init__()
        torch.manual_seed(seed)  # deterministic init per run
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc = nn.Linear(64 * 4 * 4, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)   # 32 -> 16
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)   # 16 -> 8
        x = F.max_pool2d(F.relu(self.conv3(x)), 2)   # 8 -> 4
        x = torch.flatten(x, 1)
        return self.fc(x)


# ------------------------------------------------------------------------ data

_CACHE = {}


def load_splits_cifar():
    """CIFAR-10 45k/5k/10k split + CIFAR-100 test OOD probe.

    Per-channel standardization with the 45k train-split statistics; the OOD
    probe is standardized with the SAME in-distribution statistics (unknown-
    shift-at-deployment policy, as in v1/v2). Returns NCHW float32 arrays.

    Memory-frugal: works from the uint8 npz in chunks (4 GB RAM machine).
    """
    if "splits" in _CACHE:
        return _CACHE["splits"]
    d = np.load(DATA_PATH_CIFAR)
    xu = d["cifar10_train_x"]      # (50000,32,32,3) uint8, no copy
    y = d["cifar10_train_y"].astype(np.int64)

    rng = np.random.default_rng(SPLIT_SEED_CIFAR)
    idx = rng.permutation(50000)
    tr, va = idx[:45000], idx[45000:]

    # per-channel mean/std over the 45k train split, from uint8, float64
    csum = np.zeros(3, dtype=np.float64)
    csq = np.zeros(3, dtype=np.float64)
    cnt = 45000 * 32 * 32
    for i in range(0, 45000, 5000):
        blk = xu[tr[i:i + 5000]].astype(np.float64) / 255.0
        csum += blk.sum(axis=(0, 1, 2))
        csq += (blk ** 2).sum(axis=(0, 1, 2))
        del blk
    mu = csum / cnt
    sd = np.sqrt(np.maximum(csq / cnt - mu ** 2, 1e-12))

    def make_nchw(u8, sel):
        """uint8 (N,32,32,3) -> float32 (N,3,32,32) standardized, in chunks."""
        n = len(sel)
        out = np.empty((n, 3, 32, 32), dtype=np.float32)
        for i in range(0, n, 2000):
            js = sel[i:i + 2000]
            blk = u8[js].astype(np.float32) / 255.0         # (m,32,32,3)
            blk = (blk - mu.astype(np.float32)) / sd.astype(np.float32)
            out[i:i + 2000] = blk.transpose(0, 3, 1, 2)
        return out

    splits = dict(
        train_x=make_nchw(xu, tr), train_y=y[tr],
        val_x=make_nchw(xu, va), val_y=y[va],
        test_x=make_nchw(d["cifar10_test_x"], np.arange(10000)),
        test_y=d["cifar10_test_y"].astype(np.int64),
        oods={"cifar100": dict(
            x=make_nchw(d["cifar100_test_x"], np.arange(10000)),
            y=d["cifar100_test_y"].astype(np.int64))},
        mu=mu, sd=sd,
    )
    del d, xu
    _CACHE["splits"] = splits
    return splits


# -------------------------------------------------------------------- training

@dataclass
class TrainConfigCIFAR:
    epochs: int
    cycles: int = 1
    lr_max: float = 0.1
    lr_min: float = 0.0
    momentum: float = 0.9
    weight_decay: float = 1e-4
    batch_size: int = 256
    seed: int = 0
    snapshot: bool = False


def lr_at_cifar(step, cfg, steps_per_epoch):
    total_steps = cfg.epochs * steps_per_epoch
    cycle_steps = total_steps / cfg.cycles
    pos = (step % cycle_steps) / cycle_steps
    return cfg.lr_min + 0.5 * (cfg.lr_max - cfg.lr_min) * (1 + math.cos(math.pi * pos))


def train_run_cifar(cfg, splits):
    """Train one SmallCNN; identical loop structure to common.train_run."""
    X = torch.from_numpy(splits["train_x"])
    Y = torch.from_numpy(splits["train_y"])
    Xv = torch.from_numpy(splits["val_x"])
    Yv = torch.from_numpy(splits["val_y"])
    n = X.shape[0]
    spe = math.ceil(n / cfg.batch_size)

    model = SmallCNN(cfg.seed)
    opt = torch.optim.SGD(model.parameters(), lr=cfg.lr_max,
                          momentum=cfg.momentum, weight_decay=cfg.weight_decay)
    g = torch.Generator().manual_seed(cfg.seed + 1)

    snapshots, history = [], []
    for epoch in range(cfg.epochs):
        model.train()
        perm = torch.randperm(n, generator=g)
        tl, seen = 0.0, 0
        for i in range(spe):
            bidx = perm[i * cfg.batch_size:(i + 1) * cfg.batch_size]
            step = epoch * spe + i
            lr = lr_at_cifar(step, cfg, spe)
            for grp in opt.param_groups:
                grp["lr"] = lr
            opt.zero_grad()
            out = model(X[bidx])
            loss = F.cross_entropy(out, Y[bidx])
            loss.backward()
            opt.step()
            tl += loss.item() * len(bidx)
            seen += len(bidx)
        model.eval()
        with torch.no_grad():
            vlog = model(Xv)
            vnll = F.cross_entropy(vlog, Yv).item()
        history.append(dict(epoch=epoch + 1, train_loss=tl / seen,
                           val_nll=vnll, lr=lr_at_cifar((epoch + 1) * spe - 1, cfg, spe)))
        if cfg.snapshot and (epoch + 1) % (cfg.epochs // cfg.cycles) == 0:
            snapshots.append({k: v.detach().clone() for k, v in model.state_dict().items()})
    model_sd = {k: v.detach().clone() for k, v in model.state_dict().items()}
    return model_sd, snapshots, history


# ------------------------------------------------------------------ evaluation

def logits_of_cifar(sd, X, batch=2048):
    m = SmallCNN(0)
    m.load_state_dict(sd)
    m = m.to(memory_format=torch.channels_last)
    m.eval()
    outs = []
    with torch.no_grad():
        for i in range(0, len(X), batch):
            xb = torch.from_numpy(np.ascontiguousarray(X[i:i + batch]))
            xb = xb.to(memory_format=torch.channels_last)
            outs.append(m(xb).numpy())
    return np.concatenate(outs, axis=0)


def probs_of_cifar(logits):
    logits = logits.astype(np.float64)
    e = np.exp(logits - logits.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def swa_state_dicts(sds):
    out = {}
    for k in sds[0]:
        out[k] = torch.mean(torch.stack([sd[k].float() for sd in sds]), dim=0)
    return out
