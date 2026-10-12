#!/usr/bin/env python3
"""CIFAR extension figure: Fig 5 (NLL by condition + OOD AUROC).

Style matches v1/v2 (Okabe-Ito, Liberation Sans, paired seed lines, 600 dpi).
All seed-level observations shown. Source data CSV exported per panel.
"""
import glob
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
for fp in ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
           "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
    try:
        fm.fontManager.addfont(fp)
    except Exception:
        pass
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Liberation Sans", "DejaVu Sans"],
    "font.size": 7.5, "axes.linewidth": 0.6, "axes.labelsize": 7.5,
    "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 6.5, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

import paths
FIGDIR = paths.FIGURES
SDIR = f"{FIGDIR}/source_data"
os.makedirs(SDIR, exist_ok=True)

COL = {"single": "#999999", "deepens": "#0072B2", "snapshot": "#E69F00",
       "swa": "#009E73"}
MK = {"single": "o", "deepens": "s", "snapshot": "D", "swa": "^"}
LBL = {"single": "Single", "deepens": "DeepEns", "snapshot": "Snapshot",
       "swa": "SWA"}
CONDS = ["single", "deepens", "snapshot", "swa"]

rows = []
for fn in glob.glob(os.path.join(paths.RESULTS, "cifar", "experiment_cifar_*.jsonl")):
    for line in open(fn):
        rows.append(json.loads(line))
rows.sort(key=lambda r: r["seed"])
assert len(rows) >= 10, f"expected >=10 seeds, got {len(rows)}"
if len(rows) > 10:
    print(f"WARNING: {len(rows)} seeds; using the first 10")


def m(cond, metric):
    if metric.startswith("ts."):
        sub = metric.split(".", 1)[1]
        return np.array([r[cond]["ts"][sub] for r in rows[:10]], float)
    return np.array([r[cond][metric] for r in rows[:10]], float)


fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), constrained_layout=True)

# --- a: NLL by condition
ax = axes[0]
xs = np.arange(len(CONDS))
csv = []
for i, c in enumerate(CONDS):
    v = m(c, "nll")
    ax.plot([i, i], [v.min(), v.max()], color=COL[c], lw=1.4, alpha=0.55, zorder=1)
    ax.scatter(np.full(len(v), i) + np.random.default_rng(7 + i).uniform(-0.09, 0.09, len(v)),
               v, s=9, color=COL[c], marker=MK[c], alpha=0.62, zorder=2,
               edgecolors="none")
    ax.plot([i - 0.16, i + 0.16], [v.mean()] * 2, color=COL[c], lw=2.2, zorder=3)
    for x in v:
        csv.append([c, f"{x:.6f}"])
ax.set_xticks(xs)
ax.set_xticklabels([LBL[c] for c in CONDS])
ax.set_ylabel("Test NLL (nats)")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
ax.set_title("CIFAR-10 test NLL", fontsize=8, pad=4)
with open(f"{SDIR}/fig5a_cifar_nll.csv", "w") as f:
    f.write("condition,nll_seed_value\n")
    for r in csv:
        f.write(",".join(r) + "\n")

# --- b: OOD AUROC (CIFAR-100 probe, MSP)
ax = axes[1]
csv = []
for i, c in enumerate(CONDS):
    v = m(c, "auroc_msp_cifar100")
    ax.plot([i, i], [v.min(), v.max()], color=COL[c], lw=1.4, alpha=0.55, zorder=1)
    ax.scatter(np.full(len(v), i) + np.random.default_rng(11 + i).uniform(-0.09, 0.09, len(v)),
               v, s=9, color=COL[c], marker=MK[c], alpha=0.62, zorder=2,
               edgecolors="none")
    ax.plot([i - 0.16, i + 0.16], [v.mean()] * 2, color=COL[c], lw=2.2, zorder=3)
    for x in v:
        csv.append([c, f"{x:.6f}"])
ax.set_xticks(xs)
ax.set_xticklabels([LBL[c] for c in CONDS])
ax.set_ylabel("OOD AUROC (MSP)")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
ax.set_title("OOD detection, CIFAR-100 probe", fontsize=8, pad=4)
with open(f"{SDIR}/fig5b_cifar_auroc.csv", "w") as f:
    f.write("condition,auroc_seed_value\n")
    for r in csv:
        f.write(",".join(r) + "\n")

for ax, letter in zip(axes, ["a", "b"]):
    ax.text(-0.16, 1.06, letter, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top", ha="left")

fig.savefig(f"{FIGDIR}/fig5_cifar.pdf")
fig.savefig(f"{FIGDIR}/fig5_cifar.png", dpi=600)
plt.close(fig)
print("saved fig5_cifar.pdf/.png")
