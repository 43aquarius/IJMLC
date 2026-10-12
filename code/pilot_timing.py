#!/usr/bin/env python3
"""Pilot: calibrate wall-clock timing and verify training stability (train/val only).

Per the analysis plan, the test set is NOT touched here. Only train loss and
validation NLL are inspected, solely to verify the optimizer setup does not
diverge and to measure per-epoch wall time.
"""
import json
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TrainConfig, train_run, load_splits, logits_of, probs_of
import torch.nn.functional as F
import torch

# 1) timing + stability of a short cyclic run (6 epochs, 3 cycles -> snapshots at 2,4,6)
t0 = time.time()
cfg = TrainConfig(epochs=6, cycles=3, seed=0, snapshot=True)
sd, snaps, hist = train_run(cfg)
dt = time.time() - t0
print(f"6-epoch cyclic run: {dt:.1f}s total -> {dt/6:.2f}s/epoch")
for h in hist:
    print(f"  epoch {h['epoch']}: train_loss={h['train_loss']:.4f} val_nll={h['val_nll']:.4f} lr_end={h['lr']:.4f}")
print(f"snapshots collected: {len(snaps)} (expected 3)")

# 2) timing of a long single run (12 epochs, 1 cycle) to check LR 0.1 stability
t0 = time.time()
cfg2 = TrainConfig(epochs=12, cycles=1, seed=0)
sd2, _, hist2 = train_run(cfg2)
dt2 = time.time() - t0
print(f"12-epoch single-cosine run: {dt2:.1f}s -> {dt2/12:.2f}s/epoch")
for h in hist2:
    print(f"  epoch {h['epoch']}: train_loss={h['train_loss']:.4f} val_nll={h['val_nll']:.4f}")

# 3) quick check: weight averaging of snapshots produces finite weights
from common import swa_state_dicts
swa = swa_state_dicts(snaps)
finite = all(torch.isfinite(v).all().item() for v in swa.values())
print("SWA weights finite:", finite)

# extrapolate total experiment wall time
per_epoch = (dt / 6 + dt2 / 12) / 2
per_seed = 3 * 60 * per_epoch  # 3 runs x 60 epochs
print(f"per-epoch estimate: {per_epoch:.2f}s | per-seed (3x60ep): {per_seed/60:.1f} min | 5 seeds: {5*per_seed/60:.1f} min")
