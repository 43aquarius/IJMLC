#!/usr/bin/env python3
"""Verification: (a) bit-level reproducibility of seed 0; (b) entropy-score diagnosis.

Re-runs seed 0 with identical seeds. Because the pipeline is deterministic,
all metrics must exactly match results/experiment.jsonl seed 0.
Then computes raw entropy statistics explaining the AUROC-entropy inversion.
"""
import json
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    TrainConfig, train_run, load_splits, logits_of, probs_of, ens_probs,
    swa_state_dicts,
)

B, K = 60, 3
s = load_splits()
base = 10000

sd_single, _, _ = train_run(TrainConfig(epochs=B, cycles=1, seed=base + 0))
sd_cyc, snaps, _ = train_run(TrainConfig(epochs=B, cycles=K, seed=base + 0, snapshot=True))
m2, _, _ = train_run(TrainConfig(epochs=B // K, cycles=1, seed=base + 11))
m3, _, _ = train_run(TrainConfig(epochs=B // K, cycles=1, seed=base + 12))
swa_sd = swa_state_dicts(snaps)

Xtest, Xood = s["test_x"], s["ood_x"]


def entropy(p):
    return -np.sum(p * np.log(np.clip(p, 1e-12, None)), axis=1)


def report(name, p_in, p_out):
    H_in, H_out = entropy(p_in), entropy(p_out)
    msp_in, msp_out = p_in.max(1), p_out.max(1)
    print(f"{name:12s} | E[H] in={H_in.mean():.4f} out={H_out.mean():.4f} "
          f"| E[MSP] in={msp_in.mean():.4f} out={msp_out.mean():.4f} "
          f"| frac(out with H < 0.5)={np.mean(H_out < 0.5):.3f} "
          f"| frac(in with H < 0.5)={np.mean(H_in < 0.5):.3f}")
    return dict(H_in_mean=float(H_in.mean()), H_out_mean=float(H_out.mean()),
                MSP_in_mean=float(msp_in.mean()), MSP_out_mean=float(msp_out.mean()))


out = {}
p_single = probs_of(logits_of(sd_single, Xtest))
p_single_o = probs_of(logits_of(sd_single, Xood))
out["single"] = report("single", p_single, p_single_o)

dm = [snaps[0], m2, m3]
p_de = ens_probs([probs_of(logits_of(sd, Xtest)) for sd in dm])
p_de_o = ens_probs([probs_of(logits_of(sd, Xood)) for sd in dm])
out["deepens"] = report("deepens", p_de, p_de_o)

p_sn = ens_probs([probs_of(logits_of(sd, Xtest)) for sd in snaps])
p_sn_o = ens_probs([probs_of(logits_of(sd, Xood)) for sd in snaps])
out["snapshot"] = report("snapshot", p_sn, p_sn_o)

p_sw = probs_of(logits_of(swa_sd, Xtest))
p_sw_o = probs_of(logits_of(swa_sd, Xood))
out["swa"] = report("swa", p_sw, p_sw_o)

# --- reproducibility check against experiment.jsonl seed 0
from common import evaluate_predictor
ref = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "experiment.jsonl"))][0]
repro = {}
for name, (pt, po) in dict(single=(p_single, p_single_o),
                           deepens=(p_de, p_de_o),
                           snapshot=(p_sn, p_sn_o),
                           swa=(p_sw, p_sw_o)).items():
    now = evaluate_predictor(pt, s, po)
    for m in ["nll", "acc", "ece15", "auroc_msp", "auroc_ent", "brier"]:
        match = abs(now[m] - ref[name][m]) < 1e-12
        repro[f"{name}.{m}"] = dict(recomputed=now[m], recorded=ref[name][m], exact_match=match)
        if not match:
            print(f"MISMATCH {name}.{m}: {now[m]} vs {ref[name][m]}")
all_ok = all(v["exact_match"] for v in repro.values())
print(f"\nBit-level reproducibility of seed 0: {'PASS' if all_ok else 'FAIL'} "
      f"({sum(v['exact_match'] for v in repro.values())}/{len(repro)} metrics exact)")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "verification_seed0.json"), "w") as f:
    json.dump(dict(entropy_stats=out, reproducibility=repro, reproducibility_pass=all_ok), f, indent=1)
