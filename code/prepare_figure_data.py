#!/usr/bin/env python3
"""Prepare aggregated figure data from raw experiment outputs -> results/figure_data.json"""
import json

import numpy as np

ROWS = [json.loads(l) for l in open("/home/z/my-project/results/experiment.jsonl")]
SD = [json.loads(l) for l in open("/home/z/my-project/results/experiment_swa_dense.jsonl")]
CONDS = ["single", "deepens", "snapshot", "swa"]


def seed_vals(cond, metric, rows=ROWS):
    return [r[cond].get(metric) for r in rows]


out = {}

# per-seed metric tables (for paired dot plots + source data)
for m in ["nll", "acc", "brier", "ece15", "auroc_msp", "disagreement_jsd",
          "member_mean_nll", "member_mean_acc"]:
    out[f"seeds_{m}"] = {c: seed_vals(c, m) for c in CONDS}
out["seeds_swa_dense"] = {
    "nll": [r["nll"] for r in SD],
    "acc": [r["acc"] for r in SD],
    "ece15": [r["ece15"] for r in SD],
    "auroc_msp": [r["auroc_msp"] for r in SD],
}

# reliability diagrams (mean across seeds per bin)
rel = {}
for c in CONDS:
    acc = np.array([r[c]["reliability15"]["bin_acc"] for r in ROWS], dtype=float)  # seeds x 15
    cnf = np.array([r[c]["reliability15"]["bin_conf"] for r in ROWS], dtype=float)
    cnt = np.array([r[c]["reliability15"]["bin_count"] for r in ROWS], dtype=float)
    with np.errstate(invalid="ignore"):
        m_acc = np.nanmean(acc, axis=0)
        m_cnf = np.nanmean(cnf, axis=0)
    rel[c] = dict(bin_acc=[None if np.isnan(v) else float(v) for v in m_acc],
                  bin_conf=[None if np.isnan(v) else float(v) for v in m_cnf],
                  bin_count=[float(v) for v in cnt.mean(axis=0)],
                  per_seed_acc=[[None if np.isnan(v) else float(v) for v in row] for row in acc],
                  per_seed_conf=[[None if np.isnan(v) else float(v) for v in row] for row in cnf])
out["reliability"] = rel

# MSP histograms (mean across seeds, normalized to density)
hist = {}
edges = np.linspace(0, 1, 41)
for c in CONDS:
    hin = np.array([r[c]["msp_hist_in"] for r in ROWS], dtype=float)
    hout = np.array([r[c]["msp_hist_out"] for r in ROWS], dtype=float)
    # normalize each seed's histogram to density then average
    din = hin / hin.sum(axis=1, keepdims=True) / (edges[1] - edges[0])
    dout = hout / hout.sum(axis=1, keepdims=True) / (edges[1] - edges[0])
    hist[c] = dict(edges=[float(e) for e in edges],
                   density_in=[float(v) for v in din.mean(axis=0)],
                   density_out=[float(v) for v in dout.mean(axis=0)])
out["msp_histograms"] = hist

# learning curves (val NLL per epoch, single + cyclic trajectories)
lc = {}
for name in ["single", "cyclic"]:
    H = np.array([[e["val_nll"] for e in r["histories"][name]] for r in ROWS])
    lc[name] = dict(mean=[float(v) for v in H.mean(axis=0)],
                    sd=[float(v) for v in H.std(axis=0, ddof=1)],
                    epochs=list(range(1, H.shape[1] + 1)))
out["learning_curves"] = lc

with open("/home/z/my-project/results/figure_data.json", "w") as f:
    json.dump(out, f)
print("figure_data.json written;",
      "reliability bins:", len(rel["single"]["bin_acc"]),
      "| curve epochs:", len(lc["single"]["mean"]))
