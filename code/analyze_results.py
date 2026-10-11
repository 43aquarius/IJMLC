#!/usr/bin/env python3
"""Pre-registered statistical analysis of the budget-matched ensemble study.

Implements research-design.md §5 exactly:
  - paired differences vs Single (DeepEns, Snapshot, SWA) + Snapshot-SWA + DeepEns-Snapshot
  - mean delta, two-sided 95% t-CI (df = n-1), exact sign-flip permutation p
  - Holm-Bonferroni across the five contrasts on the primary outcome (NLL)
  - sensitivity: ECE-10, entropy-based AUROC
Outputs: results/analysis.json, results/summary_by_condition.csv, results/contrasts.csv
"""
import itertools
import json

import numpy as np
from scipy import stats

ROWS = [json.loads(l) for l in open("/home/z/my-project/results/experiment.jsonl")]
CONDS = ["single", "deepens", "snapshot", "swa"]
CONTRASTS = [  # (name, condition A, condition B) -> metric[A] - metric[B]
    ("deepens_vs_single", "deepens", "single"),
    ("snapshot_vs_single", "snapshot", "single"),
    ("swa_vs_single", "swa", "single"),
    ("deepens_vs_snapshot", "deepens", "snapshot"),
    ("snapshot_vs_swa", "snapshot", "swa"),
]
METRICS = ["nll", "acc", "brier", "ece15", "auroc_msp"]
PRIMARY = "nll"


def vec(cond, metric):
    return np.array([r[cond].get(metric, np.nan) for r in ROWS], dtype=float)


def perm_p(d):
    """Exact two-sided sign-flip permutation test (n = len(d) <= 10)."""
    n = len(d)
    obs = abs(d.mean())
    hits = 0
    for signs in itertools.product([1, -1], repeat=n):
        if abs(np.dot(signs, d) / n) >= obs - 1e-15:
            hits += 1
    return hits / (2 ** n)


def analyze_contrast(a, b, metric):
    d = vec(a, metric) - vec(b, metric)
    n = len(d)
    mean = float(d.mean())
    sd = float(d.std(ddof=1))
    se = sd / np.sqrt(n)
    tcrit = stats.t.ppf(0.975, n - 1)
    lo, hi = mean - tcrit * se, mean + tcrit * se
    t_stat = mean / se
    p_perm = perm_p(d)
    p_t = float(2 * stats.t.sf(abs(t_stat), n - 1))
    return dict(
        A=a, B=b, metric=metric, n=n,
        mean_delta=mean, sd_delta=sd, ci95_low=float(lo), ci95_high=float(hi),
        t_stat=float(t_stat), p_t=p_t, p_perm_exact=p_perm,
        all_seed_deltas=[float(x) for x in d],
    )


def holm(pvals):
    """Holm-Bonferroni: returns adjusted p-values in original order."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


def main():
    n = len(ROWS)
    out = dict(n_seeds=n, primary=PRIMARY)

    # --- 1. per-condition summary (mean, sd, all seed values)
    out["by_condition"] = {}
    for c in CONDS:
        out["by_condition"][c] = {}
        for m in METRICS + ["ece10", "auroc_ent", "disagreement_jsd",
                            "member_mean_nll", "member_mean_acc"]:
            v = vec(c, m)
            if not np.isnan(v).all():
                out["by_condition"][c][m] = dict(
                    mean=float(v.mean()), sd=float(v.std(ddof=1)),
                    values=[float(x) for x in v],
                )

    # --- 2. contrasts on all metrics
    out["contrasts"] = {}
    for name, a, b in CONTRASTS:
        out["contrasts"][name] = {}
        for m in METRICS:
            out["contrasts"][name][m] = analyze_contrast(a, b, m)

    # --- 3. Holm on the primary family (NLL, five contrasts)
    prim = [out["contrasts"][name][PRIMARY] for name, _, _ in CONTRASTS]
    adj = holm([p["p_perm_exact"] for p in prim])
    for (name, _, _), a in zip(CONTRASTS, adj):
        out["contrasts"][name][PRIMARY]["p_holm"] = float(a)
    out["holm_family"] = [name for name, _, _ in CONTRASTS]

    # --- 4. sensitivity contrasts (ECE-10, AUROC-entropy)
    out["sensitivity"] = {}
    for name, a, b in CONTRASTS:
        out["sensitivity"][name] = {
            "ece10": analyze_contrast(a, b, "ece10"),
            "auroc_ent": analyze_contrast(a, b, "auroc_ent"),
        }

    with open("/home/z/my-project/results/analysis.json", "w") as f:
        json.dump(out, f, indent=1)

    # --- 5. human-readable report
    print("=" * 78)
    print(f"PER-CONDITION (mean ± sd, n={n}, Fashion-MNIST test, OOD=MNIST)")
    hdr = f"{'metric':<16}" + "".join(f"{c:>22}" for c in CONDS)
    print(hdr)
    for m in METRICS + ["disagreement_jsd"]:
        line = f"{m:<16}"
        for c in CONDS:
            s = out["by_condition"][c].get(m)
            line += f"{s['mean']:>12.4f} ± {s['sd']:.4f} " if s else f"{'—':>22}"
        print(line)

    print("\n" + "=" * 78)
    print("CONTRASTS on PRIMARY OUTCOME (test NLL), Holm-adjusted exact permutation p")
    for name, a, b in CONTRASTS:
        r = out["contrasts"][name][PRIMARY]
        print(f"  {name:<20} Δ={r['mean_delta']:+.4f}  95%CI [{r['ci95_low']:+.4f}, {r['ci95_high']:+.4f}]"
              f"  p_perm={r['p_perm_exact']:.4f}  p_holm={r['p_holm']:.4f}")

    print("\nCONTRASTS on secondary metrics (uncorrected, descriptive)")
    for name, a, b in CONTRASTS:
        for m in ["acc", "ece15", "auroc_msp", "brier"]:
            r = out["contrasts"][name][m]
            print(f"  {name:<20} {m:<10} Δ={r['mean_delta']:+.4f}  CI [{r['ci95_low']:+.4f}, {r['ci95_high']:+.4f}]  p={r['p_perm_exact']:.4f}")

    print("\nSENSITIVITY (ECE-10 bins / AUROC-entropy): direction checks")
    for name, a, b in CONTRASTS:
        r10 = out["sensitivity"][name]["ece10"]
        re_ = out["sensitivity"][name]["auroc_ent"]
        r15 = out["contrasts"][name]["ece15"]
        ra_ = out["contrasts"][name]["auroc_msp"]
        ok1 = np.sign(r10["mean_delta"]) == np.sign(r15["mean_delta"])
        ok2 = np.sign(re_["mean_delta"]) == np.sign(ra_["mean_delta"])
        print(f"  {name:<20} ECE10 Δ={r10['mean_delta']:+.4f} (same sign as ECE15: {ok1}) | "
              f"AUROCent Δ={re_['mean_delta']:+.4f} (same sign as AUROCmsp: {ok2})")

    # --- 6. CSV summaries
    import csv
    with open("/home/z/my-project/results/summary_by_condition.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["condition", "metric", "mean", "sd"] + [f"seed{s}" for s in range(n)])
        for c in CONDS:
            for m, s in out["by_condition"][c].items():
                w.writerow([c, m, f"{s['mean']:.6f}", f"{s['sd']:.6f}"] +
                           [f"{v:.6f}" for v in s["values"]])
    with open("/home/z/my-project/results/contrasts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["contrast", "metric", "mean_delta", "ci95_low", "ci95_high",
                    "p_perm_exact", "p_holm"])
        for name, a, b in CONTRASTS:
            for m in METRICS:
                r = out["contrasts"][name][m]
                w.writerow([name, m, f"{r['mean_delta']:.6f}", f"{r['ci95_low']:.6f}",
                            f"{r['ci95_high']:.6f}", f"{r['p_perm_exact']:.4f}",
                            f"{r.get('p_holm', '')}"])
    print("\nsaved: analysis.json, summary_by_condition.csv, contrasts.csv")


if __name__ == "__main__":
    main()
