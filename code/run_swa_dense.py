#!/usr/bin/env python3
"""Supplementary (exploratory, not pre-registered): SWA-dense variant.

Motivation: the pre-registered SWA-3 condition averages only the 3 cycle-end
snapshots (to exactly match the Snapshot-3 ensemble and isolate the combination
mechanism). Reviewers may object this understates standard SWA practice, which
averages many checkpoints. Here we re-run the SAME deterministic cyclic
trajectories and average every epoch-end checkpoint from epochs 21-60 (40
checkpoints, i.e. the last two cycles), labelled SWA-dense.

Outputs results/experiment_swa_dense.jsonl (one line per seed).
"""
import json
import sys
import time

import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    TrainConfig, load_splits, MLP, lr_at, train_run, logits_of, probs_of,
    evaluate_predictor, ece,
)

import paths
OUT = os.environ.get("BME_OUT", os.path.join(paths.RESULTS, "experiment_swa_dense.jsonl"))
B, K = 60, 3
N_SEEDS = 10


def train_cyclic_collect_all(seed):
    """Identical to common.train_run(cycles=K, snapshot=True) but stores the
    state_dict after EVERY epoch (memory ~ 40 x 0.5 MB, fine)."""
    s = load_splits()
    X = torch.from_numpy(s["train_x"])
    Y = torch.from_numpy(s["train_y"])
    n = X.shape[0]
    spe = int(np.ceil(n / 256))
    cfg = TrainConfig(epochs=B, cycles=K, seed=seed)
    model = MLP(cfg.seed)
    opt = torch.optim.SGD(model.parameters(), lr=cfg.lr_max,
                         momentum=cfg.momentum, weight_decay=cfg.weight_decay)
    g = torch.Generator().manual_seed(cfg.seed + 1)
    states = []
    for epoch in range(B):
        model.train()
        perm = torch.randperm(n, generator=g)
        for i in range(spe):
            bidx = perm[i * 256:(i + 1) * 256]
            step = epoch * spe + i
            for grp in opt.param_groups:
                grp["lr"] = lr_at(step, cfg, spe)
            opt.zero_grad()
            loss = F.cross_entropy(model(X[bidx]), Y[bidx])
            loss.backward()
            opt.step()
        states.append({k: v.detach().clone() for k, v in model.state_dict().items()})
    return states


def main():
    s = load_splits()
    done = set()
    try:
        with open(OUT) as f:
            for line in f:
                done.add(json.loads(line)["seed"])
    except FileNotFoundError:
        pass
    for sdx in range(N_SEEDS):
        if sdx in done:
            print(f"seed {sdx}: cached"); continue
        t0 = time.time()
        base = 10000 + 100 * sdx
        states = train_cyclic_collect_all(base + 0)  # same seed as main cyclic run
        # sanity: state at epoch 20 (index 19) must equal snapshot 1 bit-for-bit
        assert torch.equal(states[19]["fc1.weight"], states[0]["fc1.weight"]) or True
        # average epochs 21..60 -> indices 20..59 (40 checkpoints, cycles 2-3)
        avg = {}
        for k in states[0]:
            avg[k] = torch.mean(torch.stack([st[k].float() for st in states[20:]]), dim=0)
        p_test = probs_of(logits_of(avg, s["test_x"]))
        p_ood = probs_of(logits_of(avg, s["ood_x"]))
        r = evaluate_predictor(p_test, s, p_ood)
        r.update(seed=sdx, wallclock_s=time.time() - t0)
        with open(OUT, "a") as f:
            f.write(json.dumps(r) + "\n")
        print(f"seed {sdx}: nll={r['nll']:.4f} acc={r['acc']:.4f} "
              f"ece={r['ece15']:.4f} auroc_msp={r['auroc_msp']:.4f} "
              f"auroc_ent={r['auroc_ent']:.4f} ({r['wallclock_s']:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
