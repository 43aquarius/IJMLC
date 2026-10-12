#!/usr/bin/env python3
"""v4 independent re-analysis: OOD + temperature scaling + ECE + robustness.

Recomputes ALL statistics from raw per-seed JSONL records (not from the
released analysis JSONs), with explicitly defined multiplicity families:

  F1 (pre-registered, per digit setting): 5 contrasts x raw NLL  -> Holm
  F2 (secondary, per setting):             5 contrasts x TS-NLL  -> Holm
  OOD families (post-hoc, v4 addition):
    Oa: per (setting, probe, score):       5 contrasts           -> Holm
    Ob: per setting, both probes (MSP):    10 contrasts           -> Holm  [sensitivity]
    Oc: global across all 6 settings, MSP vs Single contrasts only? NO —
        full global 5x6=30 tests is reported descriptively as the most
        conservative view (Bonferroni-style worst case).

Also: TS effect on OOD AUROC (per condition), ECE contrasts everywhere,
leave-one-seed-out sensitivity for CIFAR, and verification that the
released analysis files match the recomputation.

Outputs: <repo>/results/v4/reanalysis_v4.json
         (plus printed human-readable report)
"""
import json
import math
import os
from itertools import combinations

import numpy as np

import paths
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(paths.RESULTS, "v4")
os.makedirs(OUT_DIR, exist_ok=True)

SETTINGS = {
    "fmnist_B60_k3":  f"{REPO}/results/v2/experiment_v2_fmnist_B60_k3.jsonl",
    "fmnist_B30_k3":  f"{REPO}/results/v2/experiment_v2_fmnist_B30_k3.jsonl",
    "fmnist_B120_k3": f"{REPO}/results/v2/experiment_v2_fmnist_B120_k3.jsonl",
    "fmnist_B60_k5":  f"{REPO}/results/v2/experiment_v2_fmnist_B60_k5.jsonl",
    "mnist_B60_k3":   f"{REPO}/results/v2/experiment_v2_mnist_B60_k3.jsonl",
    "cifar10_B60_k3": f"{REPO}/results/cifar/experiment_cifar_B60_k3.jsonl",
}
CONTRASTS = [("deepens", "single"), ("snapshot", "single"), ("swa", "single"),
             ("deepens", "snapshot"), ("snapshot", "swa")]
CONDITIONS = ["single", "deepens", "snapshot", "swa"]

# ------------------------------------------------------------------ statistics


def t_ci(deltas):
    """Mean, sd, two-sided 95% t-interval (df = n-1)."""
    a = np.asarray(deltas, dtype=np.float64)
    n = len(a)
    m = a.mean()
    s = a.std(ddof=1)
    if n < 2 or s == 0:
        return m, s, m, m
    # t quantile for df=9, 0.975 -> 2.262157...; compute per n via scipy-free approx
    try:
        from scipy import stats
        tcrit = stats.t.ppf(0.975, n - 1)
    except Exception:
        tcrit = {10: 2.2621571628, 9: 2.3060041350, 8: 2.364624252,
                 7: 2.446911851, 6: 2.570581836, 5: 2.776445105}[n - 1]
    half = tcrit * s / math.sqrt(n)
    return m, s, m - half, m + half


def perm_p_exact(deltas):
    """Exact two-sided sign-flip permutation P over all 2^n patterns.

    Statistic = |mean| of the flipped deltas. Two-sided by symmetry.
    Resolution floor with n=10: 2/1024 = 0.001953125.
    """
    a = np.asarray(deltas, dtype=np.float64)
    n = len(a)
    obs = abs(a.mean())
    idx = np.arange(1 << n, dtype=np.int64)
    # signs matrix via bit tricks (n=10 -> 1024 rows; cheap)
    signs = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(np.float64) * 2 - 1
    means = (signs @ a) / n
    count = int(np.sum(np.abs(means) >= obs - 1e-12))
    return count / float(1 << n)


def holm(pvals):
    """Holm-Bonferroni adjusted p-values (step-down)."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m, dtype=np.float64)
    running = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * pvals[i]
        running = max(running, val)
        adj[i] = min(1.0, running)
    return adj


def load_setting(path):
    recs = [json.loads(line) for line in open(path)]
    recs.sort(key=lambda r: r["seed"])
    return recs


def get_cond_metric(recs, cond, metric):
    """Per-seed values of `metric` for condition `cond`. TS metrics live in
    rec['ts'] with prefix 'ts.' removed."""
    vals = []
    for r in recs:
        if metric.startswith("ts."):
            vals.append(r[cond]["ts"][metric[3:]])
        else:
            vals.append(r[cond][metric])
    return np.asarray(vals, dtype=np.float64)


def contrast_deltas(recs, A, B, metric):
    return get_cond_metric(recs, A, metric) - get_cond_metric(recs, B, metric)


# ------------------------------------------------------------------ main pass

def main():
    report = {"settings": {}, "notes": {}}
    print("=" * 100)
    print("INDEPENDENT RE-ANALYSIS FROM RAW PER-SEED JSONL (v4)")
    print("=" * 100)

    # ---------- per-setting re-analysis ----------
    for setting, path in SETTINGS.items():
        recs = load_setting(path)
        n = len(recs)
        assert n == 10, f"{setting}: expected 10 seeds, got {n}"
        S = {"n_seeds": n,
             "seed_ids": [r["seed"] for r in recs],
             "shared_member_bit_identical":
                 next((r["shared_member_bit_identical"] for r in recs
                       if r["shared_member_bit_identical"] is not None), None),
             "metrics_by_condition": {}, "contrasts": {},
             "ood_families": {}}
        probes = recs[0]["config"]["ood_probes"]

        # --- 1. condition summaries for the key metrics
        metrics = ["nll", "ece15", "acc", "brier", "ts.nll", "ts.ece15"] + \
                  [f"auroc_msp_{p}" for p in probes] + \
                  [f"auroc_ent_{p}" for p in probes] + \
                  [f"ts.auroc_msp_{p}" for p in probes] + ["ts.T"]
        for m in metrics:
            S["metrics_by_condition"][m] = {}
            for c in CONDITIONS:
                a = get_cond_metric(recs, c, m)
                S["metrics_by_condition"][m][c] = dict(
                    mean=float(a.mean()), sd=float(a.std(ddof=1)),
                    values=[float(v) for v in a])

        # --- 2. all contrasts on the key metrics (raw P values)
        for (A, B) in CONTRASTS:
            tag = f"{A}_vs_{B}"
            S["contrasts"][tag] = {}
            for m in ["nll", "ece15", "ts.nll"] + [f"auroc_msp_{p}" for p in probes] + \
                    [f"auroc_ent_{p}" for p in probes] + [f"ts.auroc_msp_{p}" for p in probes]:
                d = contrast_deltas(recs, A, B, m)
                mm, sd, lo, hi = t_ci(d)
                S["contrasts"][tag][m] = dict(
                    mean_delta=float(mm), sd_delta=float(sd),
                    ci95_low=float(lo), ci95_high=float(hi),
                    p_perm_exact=perm_p_exact(d),
                    per_seed=[float(x) for x in d])

        # --- 3. multiplicity families
        fam = {}
        # F1: NLL family (5 contrasts)
        fam["F1_nll"] = {t: S["contrasts"][t]["nll"]["p_perm_exact"]
                         for t in S["contrasts"]}
        # F2: TS-NLL family
        fam["F2_ts_nll"] = {t: S["contrasts"][t]["ts.nll"]["p_perm_exact"]
                            for t in S["contrasts"]}
        S["holm"] = {}
        for fname, pdict in fam.items():
            keys = list(pdict.keys())
            adj = holm([pdict[k] for k in keys])
            S["holm"][fname] = {k: float(a) for k, a in zip(keys, adj)}

        # OOD families: per (probe, score) 5 contrasts
        for p in probes:
            for score in ["msp", "ent"]:
                fm = f"Oa_{score}_{p}"
                pdict = {t: S["contrasts"][t][f"auroc_{score}_{p}"]["p_perm_exact"]
                         for t in S["contrasts"]}
                keys = list(pdict.keys())
                adj = holm([pdict[k] for k in keys])
                S["holm"][fm] = {k: float(a) for k, a in zip(keys, adj)}
            # TS OOD family (sensitivity)
            fm = f"Oa_ts_msp_{p}"
            pdict = {t: S["contrasts"][t][f"ts.auroc_msp_{p}"]["p_perm_exact"]
                     for t in S["contrasts"]}
            keys = list(pdict.keys())
            adj = holm([pdict[k] for k in keys])
            S["holm"][fm] = {k: float(a) for k, a in zip(keys, adj)}

        # Ob: both probes jointly, MSP (10 tests) — digit settings only
        if len(probes) == 2:
            pdict = {}
            for p in probes:
                for t in S["contrasts"]:
                    pdict[f"{t}|{p}"] = S["contrasts"][t][f"auroc_msp_{p}"]["p_perm_exact"]
            keys = list(pdict.keys())
            adj = holm([pdict[k] for k in keys])
            S["holm"]["Ob_msp_both_probes"] = {k: float(a) for k, a in zip(keys, adj)}

        # --- 4. TS effect on OOD AUROC (per condition)
        S["ts_effect_on_ood"] = {}
        for p in probes:
            for c in CONDITIONS:
                raw = get_cond_metric(recs, c, f"auroc_msp_{p}")
                tsd = get_cond_metric(recs, c, f"ts.auroc_msp_{p}")
                dd = tsd - raw
                S["ts_effect_on_ood"][f"{c}|{p}"] = dict(
                    mean_delta=float(dd.mean()),
                    min=float(dd.min()), max=float(dd.max()),
                    per_seed=[float(x) for x in dd])

        report["settings"][setting] = S

    # ---------- global OOD sensitivity (Oc): all settings x probes x 5 contrasts, MSP ----------
    print("\n--- Global OOD multiplicity sensitivity (family Oc, post-hoc) ---")
    allp = []
    allk = []
    for setting, S in report["settings"].items():
        probes = [k.split("_")[-1] for k in
                  next(iter(S["metrics_by_condition"].values())).keys()
                  if k.startswith("auroc_msp_")]
        probes = sorted(set(p.rsplit("_", 1)[1] if "_" in p else p for p in probes))
        for p in S.get("probes_list", []):
            pass
        for m in S["metrics_by_condition"]:
            if m.startswith("auroc_msp_"):
                p = m[len("auroc_msp_"):]
                for t in S["contrasts"]:
                    allp.append(S["contrasts"][t][m]["p_perm_exact"])
                    allk.append(f"{setting}|{t}|{p}")
    keys, vals = allk, allp
    adj = holm(vals)
    report["notes"]["Oc_global_msp"] = {
        "family_size": len(vals),
        "results": {k: float(a) for k, a in zip(keys, adj)},
        "raw": {k: float(v) for k, v in zip(keys, vals)},
    }
    sig = [k for k, a in zip(keys, adj) if a < 0.05]
    print(f"  family size: {len(vals)}; surviving Holm at 0.05: {len(sig)}")
    for k in sig:
        print(f"    {k}: raw={report['notes']['Oc_global_msp']['raw'][k]:.4f} "
              f"holm={report['notes']['Oc_global_msp']['results'][k]:.4f}")

    # ---------- CIFAR leave-one-seed-out sensitivity ----------
    print("\n--- CIFAR leave-one-seed-out sensitivity (exploratory) ---")
    cif = report["settings"]["cifar10_B60_k3"]
    loo = {}
    for drop in range(10):
        keep = [i for i in range(10) if i != drop]
        recs = load_setting(SETTINGS["cifar10_B60_k3"])
        sub = [recs[i] for i in keep]

        def dv(A, B, m):
            return get_cond_metric(sub, A, m) - get_cond_metric(sub, B, m)
        loo[f"drop_seed{drop}"] = {
            f"{A}_vs_{B}|{m}": dict(
                mean_delta=float(dv(A, B, m).mean()),
                ci95_low=float(t_ci(dv(A, B, m))[2]),
                ci95_high=float(t_ci(dv(A, B, m))[3]),
                p_perm_exact=perm_p_exact(dv(A, B, m)))
            for (A, B) in CONTRASTS
            for m in ["nll", "ece15", "auroc_msp_cifar100"]
        }
    report["notes"]["cifar_leave_one_out"] = loo
    for drop in range(10):
        d = loo[f"drop_seed{drop}"]
        print(f"  drop seed {drop}: "
              f"DE-SE nll {d['deepens_vs_snapshot|nll']['mean_delta']:+.4f} "
              f"(p={d['deepens_vs_snapshot|nll']['p_perm_exact']:.4f}) | "
              f"DE-SE ece {d['deepens_vs_snapshot|ece15']['mean_delta']:+.4f} "
              f"(p={d['deepens_vs_snapshot|ece15']['p_perm_exact']:.4f}) | "
              f"SWA-SG auroc {d['swa_vs_single|auroc_msp_cifar100']['mean_delta']:+.4f} "
              f"(p={d['swa_vs_single|auroc_msp_cifar100']['p_perm_exact']:.4f})")

    # ---------- verification against released analysis ----------
    print("\n--- Verification vs released analysis files ---")
    mismatches = []
    for setting, relpath in [
        ("cifar10_B60_k3", f"{REPO}/results/cifar/analysis_cifar.json"),
    ]:
        rel = json.load(open(relpath))[setting]
        for tag, cdat in rel["contrasts"].items():
            for m, mdat in cdat.items():
                if m not in report["settings"][setting]["contrasts"][tag]:
                    continue  # only verify overlapping metrics
                mine = report["settings"][setting]["contrasts"][tag][m]
                for k in ["mean_delta", "ci95_low", "ci95_high", "p_perm_exact"]:
                    if abs(mine[k] - mdat[k]) > 1e-9:
                        mismatches.append((setting, tag, m, k, mine[k], mdat[k]))
    if mismatches:
        print(f"  {len(mismatches)} MISMATCHES vs analysis_cifar.json:")
        for mm in mismatches[:10]:
            print("   ", mm)
    else:
        print("  CIFAR: all contrast stats (mean/CI/p) reproduce analysis_cifar.json exactly")

    # v2 released analysis cross-check (spot: fmnist_B60_k3 all contrasts/metrics)
    rel2 = json.load(open(f"{REPO}/results/v2/analysis_v2.json"))["fmnist_B60_k3"]
    mm2 = 0
    for tag, cdat in rel2["contrasts"].items():
        for m, mdat in cdat.items():
            if m in report["settings"]["fmnist_B60_k3"]["contrasts"][tag]:
                mine = report["settings"]["fmnist_B60_k3"]["contrasts"][tag][m]
                for k in ["mean_delta", "ci95_low", "ci95_high", "p_perm_exact"]:
                    if abs(mine[k] - mdat[k]) > 1e-9:
                        mm2 += 1
                        print(f"  MISMATCH {tag} {m} {k}: mine={mine[k]} rel={mdat[k]}")
    if mm2 == 0:
        print("  FMNIST core: all overlapping contrast stats reproduce analysis_v2.json exactly")

    # ---------- headline OOD table ----------
    print("\n" + "=" * 100)
    print("HEADLINE: OOD AUROC (MSP) contrasts vs Single, raw & corrected")
    print("=" * 100)
    hdr = f"{'setting':16s} {'probe':8s} {'DE-SG':>22s} {'SN-SG':>22s} {'SWA-SG':>22s}"
    print(hdr)
    for setting, S in report["settings"].items():
        probes = sorted({m[len("auroc_msp_"):] for m in S["metrics_by_condition"]
                         if m.startswith("auroc_msp_")})
        for p in probes:
            row = f"{setting:16s} {p:8s}"
            for (A, B) in [("deepens", "single"), ("snapshot", "single"), ("swa", "single")]:
                tag = f"{A}_vs_{B}"
                d = S["contrasts"][tag][f"auroc_msp_{p}"]
                hol = S["holm"].get(f"Oa_msp_{p}", {}).get(tag, float("nan"))
                row += (f"  {d['mean_delta']:+.4f} p={d['p_perm_exact']:.4f}"
                        f"/H{hol:.4f}")
            print(row)

    # SWA detail rows across everything
    print("\nSWA vs Single on OOD (all settings, MSP):")
    for setting, S in report["settings"].items():
        for p in sorted({m[len("auroc_msp_"):] for m in S["metrics_by_condition"]
                         if m.startswith("auroc_msp_")}):
            d = S["contrasts"]["swa_vs_single"][f"auroc_msp_{p}"]
            hol = S["holm"].get(f"Oa_msp_{p}", {}).get("swa_vs_single")
            hol_b = S["holm"].get("Ob_msp_both_probes", {}).get(f"swa_vs_single|{p}")
            oc = report["notes"]["Oc_global_msp"]["results"].get(
                f"{setting}|swa_vs_single|{p}")
            print(f"  {setting:16s} {p:8s} Δ={d['mean_delta']:+.4f} "
                  f"CI=[{d['ci95_low']:+.4f},{d['ci95_high']:+.4f}] "
                  f"raw={d['p_perm_exact']:.4f} H(family)={hol:.4f} "
                  f"H(setting)={hol_b if hol_b is not None else float('nan'):.4f} "
                  f"H(global)={oc if oc is not None else float('nan'):.4f}")

    # TS effect on OOD summary
    print("\nTS effect on OOD AUROC (Δ = TS − raw, per condition; means over seeds):")
    for setting, S in report["settings"].items():
        items = [f"{k}: {v['mean_delta']:+.4f} [{v['min']:+.4f},{v['max']:+.4f}]"
                 for k, v in S["ts_effect_on_ood"].items()]
        print(f"  {setting}: " + " | ".join(items))

    # ECE contrasts everywhere
    print("\nECE15 contrasts (DeepEns − Snapshot and DeepEns − Single):")
    for setting, S in report["settings"].items():
        d1 = S["contrasts"]["deepens_vs_snapshot"]["ece15"]
        d2 = S["contrasts"]["deepens_vs_single"]["ece15"]
        print(f"  {setting:16s} DE-SN {d1['mean_delta']:+.4f} "
              f"[{d1['ci95_low']:+.4f},{d1['ci95_high']:+.4f}] p={d1['p_perm_exact']:.4f} | "
              f"DE-SG {d2['mean_delta']:+.4f} "
              f"[{d2['ci95_low']:+.4f},{d2['ci95_high']:+.4f}] p={d2['p_perm_exact']:.4f}")

    with open(f"{OUT_DIR}/reanalysis_v4.json", "w") as f:
        json.dump(report, f, indent=1)
    print(f"\nSaved: {OUT_DIR}/reanalysis_v4.json")


if __name__ == "__main__":
    main()
