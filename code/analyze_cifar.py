#!/usr/bin/env python3
"""Statistical analysis of the CIFAR cross-architecture extension.

Identical machinery to analyze_v2.py (same five contrasts, exact sign-flip
permutation tests, Holm families on raw NLL and TS-NLL); reads
results/cifar/experiment_cifar_*.jsonl, writes analysis_cifar.json,
summary_cifar.csv, contrasts_cifar.csv.

This extension is POST-HOC (not pre-registered); labelled as such in the
paper. Statistical plan was fixed in research-docs/experiment-plan-cifar.md
before any test-set evaluation.
"""
import csv
import glob
import itertools
import json
import os

import numpy as np
from scipy import stats

import paths

CDIR = os.environ.get("BME_CIFARDIR", os.path.join(paths.RESULTS, "cifar"))
CONDS = ["single", "deepens", "snapshot", "swa"]
CONTRASTS = [
    ("deepens_vs_single", "deepens", "single"),
    ("snapshot_vs_single", "snapshot", "single"),
    ("swa_vs_single", "swa", "single"),
    ("deepens_vs_snapshot", "deepens", "snapshot"),
    ("snapshot_vs_swa", "snapshot", "swa"),
]
BASE_METRICS = ["nll", "acc", "brier", "ece15", "ece10"]


def perm_p(d):
    n = len(d)
    obs = abs(d.mean())
    hits = 0
    for signs in itertools.product([1, -1], repeat=n):
        if abs(np.dot(signs, d) / n) >= obs - 1e-15:
            hits += 1
    return hits / (2 ** n)


def holm(pvals):
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


def vec(rows, cond, metric):
    if metric.startswith("ts."):
        sub = metric.split(".", 1)[1]
        return np.array([r[cond]["ts"].get(sub, np.nan) for r in rows], float)
    return np.array([r[cond].get(metric, np.nan) for r in rows], float)


def analyze_contrast(rows, a, b, metric):
    d = vec(rows, a, metric) - vec(rows, b, metric)
    n = len(d)
    mean = float(d.mean())
    sd = float(d.std(ddof=1))
    se = sd / np.sqrt(n)
    tcrit = stats.t.ppf(0.975, n - 1)
    lo, hi = mean - tcrit * se, mean + tcrit * se
    t_stat = mean / se
    return dict(
        A=a, B=b, metric=metric, n=n,
        mean_delta=mean, sd_delta=sd, ci95_low=float(lo), ci95_high=float(hi),
        t_stat=float(t_stat),
        p_t=float(2 * stats.t.sf(abs(t_stat), n - 1)),
        p_perm_exact=perm_p(d),
        all_seed_deltas=[float(x) for x in d],
    )


def metrics_for(rows):
    ms = list(BASE_METRICS)
    for m in BASE_METRICS:
        ms.append(f"ts.{m}")
    probes = rows[0]["config"]["ood_probes"]
    for p in probes:
        ms += [f"auroc_msp_{p}", f"auroc_ent_{p}", f"ts.auroc_msp_{p}"]
    ms += ["disagreement_jsd", "member_mean_nll", "member_mean_acc", "ts.T"]
    return ms


def analyze_setting(rows, tag):
    out = dict(tag=tag, n_seeds=len(rows), config=rows[0]["config"],
              shared_member_bit_identical=rows[0].get("shared_member_bit_identical"))
    mets = metrics_for(rows)
    out["by_condition"] = {}
    for c in CONDS:
        out["by_condition"][c] = {}
        for m in mets:
            v = vec(rows, c, m)
            if not np.isnan(v).all():
                out["by_condition"][c][m] = dict(
                    mean=float(v.mean()), sd=float(v.std(ddof=1)),
                    values=[float(x) for x in v])
    out["contrasts"] = {}
    for name, a, b in CONTRASTS:
        out["contrasts"][name] = {}
        for m in mets:
            if m in ("ts.T", "disagreement_jsd", "member_mean_nll", "member_mean_acc"):
                continue
            out["contrasts"][name][m] = analyze_contrast(rows, a, b, m)
    for family, key in [("nll", "p_holm"), ("ts.nll", "p_holm_ts")]:
        prim = [out["contrasts"][name][family] for name, _, _ in CONTRASTS]
        adj = holm([p["p_perm_exact"] for p in prim])
        for (name, _, _), a_ in zip(CONTRASTS, adj):
            out["contrasts"][name][family][key] = float(a_)
    return out


def main():
    files = sorted(glob.glob(os.path.join(CDIR, "experiment_cifar_*.jsonl")))
    assert files, f"no cifar result files in {CDIR}"
    settings = {}
    for fn in files:
        for line in open(fn):
            r = json.loads(line)
            cfg = r["config"]
            key = (cfg["id"], cfg["budget"], cfg["k"])
            settings.setdefault(key, []).append(r)

    all_out = {}
    for key in sorted(settings):
        rows = sorted(settings[key], key=lambda r: r["seed"])
        seeds = [r["seed"] for r in rows]
        assert len(seeds) == len(set(seeds)), f"duplicate seeds in {key}"
        tag = f"{key[0]}_B{key[1]}_k{key[2]}"
        all_out[tag] = analyze_setting(rows, tag)
        s = all_out[tag]
        print("=" * 78)
        print(f"SETTING {tag}  (n={s['n_seeds']} seeds, probes={s['config']['ood_probes']})")
        for m in ["nll", "acc", "ece15", "ts.nll", "ts.ece15"] + \
                 [f"auroc_msp_{p}" for p in s["config"]["ood_probes"]]:
            line = f"  {m:<18}"
            for c in CONDS:
                v = s["by_condition"][c].get(m)
                line += f"{v['mean']:>11.4f}" if v else f"{'—':>11}"
            print(line + "   (single/deepens/snapshot/swa)")
        for name, _, _ in CONTRASTS:
            r = s["contrasts"][name]["nll"]
            print(f"  {name:<20} ΔNLL={r['mean_delta']:+.4f} "
                  f"[{r['ci95_low']:+.4f},{r['ci95_high']:+.4f}] "
                  f"p_holm={r.get('p_holm', float('nan')):.4f} | "
                  f"ΔTS-NLL={s['contrasts'][name]['ts.nll']['mean_delta']:+.4f} "
                  f"p_holm_ts={s['contrasts'][name]['ts.nll'].get('p_holm_ts', float('nan')):.4f}")
        print(f"  mechanism: member NLL DE={s['by_condition']['deepens']['member_mean_nll']['mean']:.4f} "
              f"SN={s['by_condition']['snapshot']['member_mean_nll']['mean']:.4f} | "
              f"JSD DE={s['by_condition']['deepens']['disagreement_jsd']['mean']:.4f} "
              f"SN={s['by_condition']['snapshot']['disagreement_jsd']['mean']:.4f}")

    with open(os.path.join(CDIR, "analysis_cifar.json"), "w") as f:
        json.dump(all_out, f, indent=1)
    with open(os.path.join(CDIR, "summary_cifar.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["setting", "condition", "metric", "mean", "sd", "n"])
        for tag, s in all_out.items():
            for c in CONDS:
                for m, v in s["by_condition"][c].items():
                    w.writerow([tag, c, m, f"{v['mean']:.6f}",
                                f"{v['sd']:.6f}", s["n_seeds"]])
    with open(os.path.join(CDIR, "contrasts_cifar.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["setting", "contrast", "metric", "mean_delta", "ci95_low",
                    "ci95_high", "p_perm_exact", "p_holm", "p_holm_ts"])
        for tag, s in all_out.items():
            for name, _, _ in CONTRASTS:
                for m, r in s["contrasts"][name].items():
                    w.writerow([tag, name, m, f"{r['mean_delta']:.6f}",
                                f"{r['ci95_low']:.6f}", f"{r['ci95_high']:.6f}",
                                f"{r['p_perm_exact']:.4f}",
                                r.get("p_holm", ""), r.get("p_holm_ts", "")])
    print(f"\nsaved: {CDIR}/analysis_cifar.json, summary_cifar.csv, contrasts_cifar.csv")


if __name__ == "__main__":
    main()
