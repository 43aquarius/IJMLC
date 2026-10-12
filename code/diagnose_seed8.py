#!/usr/bin/env python3
"""Diagnostic re-run of CIFAR seed 8 (anomalous DeepEns replicate).

Reproduces the three budget-split ensemble members EXACTLY as
run_experiments_cifar.py::train_piece does (channels_last, same seeds,
same optimizer/schedule/data order), with per-epoch logging, and then
evaluates each member individually on the test set.

Seed conventions for s=8, base=10800:
  member 1 = first cyclic snapshot  -> seed 10800 (= standalone 20-epoch run)
  member 2 (m1)                     -> seed 10812
  member 3 (m2)                     -> seed 10813

Gate: ensemble metrics must match the released JSONL record for seed 8
(deepens NLL 0.92898..., member_mean_nll 1.41067..., member_mean_acc
0.51463..., JSD 0.32879...). If they do, per-member numbers are trustworthy.
"""
import json
import math
import os
import sys

import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import nll, accuracy, ece, pairwise_jsd  # noqa: E402
from common_cifar import (load_splits_cifar, TrainConfigCIFAR,  # noqa: E402
                          SmallCNN, probs_of_cifar, lr_at_cifar)

torch.set_num_threads(2)
import paths
OUT = os.path.join(paths.RESULTS, "v4", "seed8_diagnosis.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

B, K = 60, 3
ME = B // K  # 20


def train_member(cfg_seed, splits, label):
    """train_piece replica (fresh-start branch), with logging."""
    cfg = TrainConfigCIFAR(epochs=ME, cycles=1, seed=cfg_seed)
    model = SmallCNN(cfg.seed)
    model = model.to(memory_format=torch.channels_last)
    opt = torch.optim.SGD(model.parameters(), lr=cfg.lr_max,
                          momentum=cfg.momentum, weight_decay=cfg.weight_decay)
    g = torch.Generator().manual_seed(cfg.seed + 1)
    X = torch.from_numpy(splits["train_x"]).to(memory_format=torch.channels_last)
    Y = torch.from_numpy(splits["train_y"])
    Xv = torch.from_numpy(splits["val_x"]).to(memory_format=torch.channels_last)
    Yv = torch.from_numpy(splits["val_y"])
    n = X.shape[0]
    spe = int(np.ceil(n / cfg.batch_size))
    history = []
    for epoch in range(cfg.epochs):
        model.train()
        perm = torch.randperm(n, generator=g)
        tl, seen, maxlogit = 0.0, 0, 0.0
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
            maxlogit = max(maxlogit, float(out.abs().max()))
        model.eval()
        with torch.no_grad():
            vnll = F.cross_entropy(model(Xv), Yv).item()
            # accuracy on val for shape of the failure
            vacc = float((model(Xv).argmax(1) == Yv).float().mean())
        history.append(dict(epoch=epoch + 1, train_loss=tl / seen,
                            val_nll=vnll, val_acc=vacc,
                            lr=lr_at_cifar((epoch + 1) * spe - 1, cfg, spe),
                            max_abs_logit=maxlogit))
        print(f"  [{label}] epoch {epoch+1:2d}: train_loss={tl/seen:.4f} "
              f"val_nll={vnll:.4f} val_acc={vacc:.4f} max|logit|={maxlogit:.1f}",
              flush=True)
    model_sd = {k: v.detach().clone() for k, v in model.state_dict().items()}
    return model_sd, history


def probs_of(sd, X):
    m = SmallCNN(0)
    m.load_state_dict(sd)
    m = m.to(memory_format=torch.channels_last)
    m.eval()
    outs = []
    with torch.no_grad():
        for i in range(0, len(X), 2048):
            xb = torch.from_numpy(np.ascontiguousarray(X[i:i + 2048]))
            xb = xb.to(memory_format=torch.channels_last)
            outs.append(m(xb).numpy())
    logits = np.concatenate(outs, axis=0)
    return probs_of_cifar(logits)


def main():
    print("loading splits...", flush=True)
    splits = load_splits_cifar()
    Xtest, ytest = splits["test_x"], splits["test_y"]

    members = {}
    member_probs = {}
    for label, seed in [("member1(shared,seed10800)", 10800),
                        ("member2(m1,seed10812)", 10812),
                        ("member3(m2,seed10813)", 10813)]:
        print(f"\n=== training {label} ===", flush=True)
        sd, hist = train_member(seed, splits, label)
        p_test = probs_of(sd, Xtest)
        member_probs[label] = p_test
        members[label] = dict(
            seed=seed, history=hist,
            test_nll=nll(p_test, ytest),
            test_acc=accuracy(p_test, ytest),
            test_ece15=ece(p_test, ytest, 15),
            mean_confidence=float(p_test.max(axis=1).mean()),
        )
        m = members[label]
        print(f"  => {label}: NLL={m['test_nll']:.4f} acc={m['test_acc']:.4f} "
              f"ECE15={m['test_ece15']:.4f} mean_MSP={m['mean_confidence']:.4f}",
              flush=True)

    # ensemble = mean of the three members
    ens = np.mean(np.stack(list(member_probs.values()), axis=0), axis=0)
    ens_nll = nll(ens, ytest)
    mm_nll = float(np.mean([members[k]["test_nll"] for k in members]))
    mm_acc = float(np.mean([members[k]["test_acc"] for k in members]))
    jsd = pairwise_jsd(list(member_probs.values()))
    result = dict(members=members,
                  ensemble=dict(nll=ens_nll, acc=accuracy(ens, ytest),
                                ece15=ece(ens, ytest, 15),
                                member_mean_nll=mm_nll, member_mean_acc=mm_acc,
                                disagreement_jsd=jsd),
                  released_record=dict(nll=0.9289849824382185,
                                       member_mean_nll=1.4106702769638764,
                                       member_mean_acc=0.5146333333333334,
                                       disagreement_jsd=0.32879137234349526),
                  gate_pass=dict(
                      nll=abs(ens_nll - 0.9289849824382185) < 1e-6,
                      member_mean_nll=abs(mm_nll - 1.4106702769638764) < 1e-6,
                      member_mean_acc=abs(mm_acc - 0.5146333333333334) < 1e-6,
                      jsd=abs(jsd - 0.32879137234349526) < 1e-9))
    print(f"\n=== ENSEMBLE CHECK ===")
    print(f"  ens NLL {ens_nll:.6f} (released 0.928985)")
    print(f"  member_mean_nll {mm_nll:.6f} (released 1.410670)")
    print(f"  member_mean_acc {mm_acc:.6f} (released 0.514633)")
    print(f"  JSD {jsd:.6f} (released 0.328791)")
    print(f"  GATE: {result['gate_pass']}")
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print("saved", OUT)

if __name__ == "__main__":
    main()
