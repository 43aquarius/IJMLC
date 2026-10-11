#!/usr/bin/env python3
"""v2 extension figures: budget/size robustness, temperature scaling, cross-dataset.

Style matches v1 (Okabe-Ito, Liberation Sans, paired seed dots, 600 dpi).
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

FIGDIR = "/home/z/my-project/figures"
SDIR = f"{FIGDIR}/source_data"
os.makedirs(SDIR, exist_ok=True)

COL = {"single": "#999999", "deepens": "#0072B2", "snapshot": "#E69F00",
       "swa": "#009E73"}
MK = {"single": "o", "deepens": "s", "snapshot": "D", "swa": "^"}
LBL = {"single": "Single", "deepens": "DeepEns", "snapshot": "Snapshot",
       "swa": "SWA"}
CONDS = ["single", "deepens", "snapshot", "swa"]

# ----------------------------------------------------------------- data
def load(tag):
    rows = []
    for fn in glob.glob(f"/home/z/my-project/results/v2/experiment_v2_{tag}*.jsonl"):
        for line in open(fn):
            rows.append(json.loads(line))
    rows.sort(key=lambda r: r["seed"])
    return rows

DATA = {
    "fmnist_B60_k3": load("fmnist_B60_k3"),
    "fmnist_B30_k3": load("fmnist_B30_k3"),
    "fmnist_B120_k3": load("fmnist_B120_k3"),
    "fmnist_B60_k5": load("fmnist_B60_k5"),
    "mnist_B60_k3": load("mnist_B60_k3"),
}
for k, v in DATA.items():
    assert len(v) == 10, (k, len(v))


def m(tag, cond, metric):
    if metric.startswith("ts."):
        sub = metric.split(".", 1)[1]
        return np.array([r[cond]["ts"][sub] for r in DATA[tag]], float)
    return np.array([r[cond][metric] for r in DATA[tag]], float)


def save(fig, name, dpi=600):
    fig.savefig(f"{FIGDIR}/{name}.pdf")
    fig.savefig(f"{FIGDIR}/{name}.png", dpi=dpi)
    plt.close(fig)
    print(f"saved {name}.pdf/.png")


def panel_letter(ax, letter):
    ax.text(-0.16, 1.06, letter, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top", ha="left")


def export_csv(name, header, rows):
    with open(f"{SDIR}/{name}", "w") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")


# ============================================================== Fig 2: budget & size
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), constrained_layout=True)

# --- a: NLL vs budget
ax = axes[0]
budgets = [30, 60, 120]
tags_b = ["fmnist_B30_k3", "fmnist_B60_k3", "fmnist_B120_k3"]
csv_rows = []
for c in CONDS:
    means = [m(t, c, "nll").mean() for t in tags_b]
    sds = [m(t, c, "nll").std(ddof=1) for t in tags_b]
    ax.errorbar([0, 1, 2], means, yerr=sds, color=COL[c], marker=MK[c],
                ms=4.5, lw=1.2, elinewidth=0.8, capsize=2, label=LBL[c])
    for x, mu in zip([0, 1, 2], means):
        ax.annotate(f"{mu:.3f}", (x, mu), xytext=(4, -1), textcoords="offset points",
                    fontsize=5.8, color=COL[c])
    for x, t in zip([0, 1, 2], tags_b):
        csv_rows.append([c, budgets[x],
                         f"{m(t, c, 'nll').mean():.6f}",
                         f"{m(t, c, 'nll').std(ddof=1):.6f}"])
export_csv("fig2a_budget_nll.csv",
           ["condition", "budget_epochs", "nll_mean", "nll_sd"], csv_rows)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["30", "60", "120"])
ax.set_xlabel("Total budget B (epochs)")
ax.set_ylabel("Test NLL (nats)")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper left", handlelength=1.4, labelspacing=0.3)
panel_letter(ax, "a")

# --- b: ensemble size k=3 vs k=5
ax = axes[1]
csv_rows = []
for c in CONDS:
    v3 = m("fmnist_B60_k3", c, "nll")
    v5 = m("fmnist_B60_k5", c, "nll")
    for s in range(10):
        ax.plot([0, 1], [v3[s], v5[s]], color=COL[c], lw=0.5, alpha=0.35, zorder=1)
    ax.scatter(np.zeros(10), v3, s=8, color=COL[c], marker=MK[c], alpha=0.5,
               linewidths=0, zorder=2)
    ax.scatter(np.ones(10), v5, s=8, color=COL[c], marker=MK[c], alpha=0.5,
               linewidths=0, zorder=2)
    ax.scatter([0], [v3.mean()], s=46, color=COL[c], marker=MK[c],
               edgecolor="black", linewidths=0.7, zorder=3)
    ax.scatter([1], [v5.mean()], s=46, color=COL[c], marker=MK[c],
               edgecolor="black", linewidths=0.7, zorder=3)
    csv_rows.append([c, "3", f"{v3.mean():.6f}", f"{v3.std(ddof=1):.6f}"])
    csv_rows.append([c, "5", f"{v5.mean():.6f}", f"{v5.std(ddof=1):.6f}"])
export_csv("fig2b_ensemble_size_nll.csv",
           ["condition", "k", "nll_mean", "nll_sd"], csv_rows)
ax.set_xticks([0, 1])
ax.set_xticklabels(["k = 3", "k = 5"])
ax.set_xlim(-0.35, 1.35)
ax.set_xlabel("Ensemble size (B = 60 epochs throughout)")
ax.set_ylabel("Test NLL (nats)")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
panel_letter(ax, "b")
save(fig, "fig2_robustness")

# ============================================================== Fig 3: temperature scaling
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), constrained_layout=True)

# --- a: raw -> TS NLL dumbbell per condition (main setting)
ax = axes[0]
csv_rows = []
for i, c in enumerate(CONDS):
    raw = m("fmnist_B60_k3", c, "nll")
    ts = m("fmnist_B60_k3", c, "ts.nll")
    for s in range(10):
        ax.plot([i - 0.16, i + 0.16], [raw[s], ts[s]], color=COL[c], lw=0.5,
                alpha=0.3, zorder=1)
    ax.scatter(np.full(10, i - 0.16), raw, s=8, color=COL[c], marker=MK[c],
               alpha=0.5, linewidths=0, zorder=2)
    ax.scatter(np.full(10, i + 0.16), ts, s=8, color="none", marker=MK[c],
               alpha=0.5, edgecolors=COL[c], linewidths=0.7, zorder=2)
    mr, mt = raw.mean(), ts.mean()
    ax.scatter([i - 0.16], [mr], s=46, color=COL[c], marker=MK[c],
               edgecolor="black", linewidths=0.7, zorder=3)
    ax.scatter([i + 0.16], [mt], s=46, color="white", marker=MK[c],
               edgecolor=COL[c], linewidths=1.0, zorder=3)
    csv_rows.append([c, f"{mr:.6f}", f"{raw.std(ddof=1):.6f}",
                     f"{mt:.6f}", f"{ts.std(ddof=1):.6f}"])
export_csv("fig3a_ts_nll.csv",
           ["condition", "nll_mean", "nll_sd", "ts_nll_mean", "ts_nll_sd"], csv_rows)
ax.set_xticks(range(4))
ax.set_xticklabels([LBL[c] for c in CONDS], fontsize=6.8)
ax.set_xlim(-0.55, 3.55)
ax.set_ylabel("Test NLL (nats)")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
ax.text(0.02, 0.02, "filled = uncalibrated   open = after TS",
        transform=ax.transAxes, fontsize=6.0, color="#444444")
panel_letter(ax, "a")

# --- b: fitted temperature per condition
ax = axes[1]
csv_rows = []
for i, c in enumerate(CONDS):
    T = m("fmnist_B60_k3", c, "ts.T")
    for s in range(10):
        ax.plot([i], [T[s]], marker=MK[c], ms=4, color=COL[c], alpha=0.5,
                ls="none")
    ax.plot([i - 0.12, i + 0.12], [T.mean()] * 2, color=COL[c], lw=1.8)
    csv_rows.append([c, f"{T.mean():.4f}", f"{T.std(ddof=1):.4f}"])
export_csv("fig3b_fitted_T.csv", ["condition", "T_mean", "T_sd"], csv_rows)
ax.axhline(1.0, color="#888888", lw=0.8, ls=":")
ax.text(3.42, 1.03, "T = 1", fontsize=6.2, color="#666666", ha="right")
ax.set_xticks(range(4))
ax.set_xticklabels([LBL[c] for c in CONDS], fontsize=6.8)
ax.set_xlim(-0.55, 3.55)
ax.set_ylabel("Fitted temperature $\\hat{T}$")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
panel_letter(ax, "b")
save(fig, "fig3_temperature")

# ============================================================== Fig 4: direction & probes
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), constrained_layout=True)

# --- a: MNIST-ID NLL with significance
ax = axes[0]
csv_rows = []
V = np.array([m("mnist_B60_k3", c, "nll") for c in CONDS])
for s in range(10):
    ax.plot(range(4), V[:, s], color="#BBBBBB", lw=0.5, alpha=0.7, zorder=1)
for i, c in enumerate(CONDS):
    ax.scatter(np.full(10, i), V[i], s=9, color=COL[c], marker=MK[c],
               alpha=0.55, linewidths=0, zorder=2)
    ax.scatter([i], [V[i].mean()], s=46, color=COL[c], marker=MK[c],
               edgecolor="black", linewidths=0.7, zorder=3)
    csv_rows.append([c, f"{V[i].mean():.6f}", f"{V[i].std(ddof=1):.6f}"])
export_csv("fig4a_mnist_nll.csv", ["condition", "nll_mean", "nll_sd"], csv_rows)
ax.set_xticks(range(4))
ax.set_xticklabels([LBL[c] for c in CONDS], fontsize=6.8)
ax.set_xlim(-0.45, 3.45)
ax.set_ylabel("Test NLL on MNIST (nats)")
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
# significance annotations vs Single (Holm-adjusted exact permutation p)
ann = [(1, 0.0098, "*"), (2, 0.4062, "n.s."), (3, 0.4062, "n.s.")]
ymax = V.max()
for i, p, txt in ann:
    ax.annotate(f"p={p:.4f} {txt}" if txt == "*" else f"p={p:.2f} (n.s.)",
                (i, V[i].mean()), xytext=(0, 14), textcoords="offset points",
                fontsize=5.8, ha="center", color="#333333")
ax.set_ylim(None, ymax + 0.006)
panel_letter(ax, "a")

# --- b: OOD AUROC overview across four ID->probe scenarios
ax = axes[1]
scen = [
    ("fmnist_B60_k3", "auroc_msp_mnist", "FMNIST\n→ MNIST"),
    ("fmnist_B60_k3", "auroc_msp_kmnist", "FMNIST\n→ KMNIST"),
    ("mnist_B60_k3", "auroc_msp_fmnist", "MNIST\n→ FMNIST"),
    ("mnist_B60_k3", "auroc_msp_kmnist", "MNIST\n→ KMNIST"),
]
csv_rows = []
for gi, (tag, metric, title) in enumerate(scen):
    for ci, c in enumerate(CONDS):
        v = m(tag, c, metric)
        x = gi + (ci - 1.5) * 0.19
        ax.scatter(np.full(10, x), v, s=6, color=COL[c], marker=MK[c],
                  alpha=0.45, linewidths=0, zorder=2)
        ax.scatter([x], [v.mean()], s=40, color=COL[c], marker=MK[c],
                   edgecolor="black", linewidths=0.7, zorder=3)
        csv_rows.append([title.replace("\n", "->"), LBL[c],
                         f"{v.mean():.6f}", f"{v.std(ddof=1):.6f}"])
export_csv("fig4b_ood_overview.csv",
           ["scenario", "condition", "auroc_msp_mean", "auroc_msp_sd"], csv_rows)
ax.axhline(0.5, color="#888888", lw=0.8, ls=":")
ax.text(3.46, 0.507, "chance", fontsize=6.0, color="#666666", ha="right")
ax.set_xticks(range(4))
ax.set_xticklabels([t for _, _, t in scen], fontsize=6.4)
ax.set_ylabel("OOD-detection AUROC (MSP)")
ax.set_xlabel("In-distribution task → OOD probe")
ax.set_xlim(-0.62, 3.62)
ax.set_ylim(0.45, 1.0)
ax.grid(axis="y", lw=0.35, color="#E6E6E6")
ax.set_axisbelow(True)
handles = [plt.Line2D([], [], color=COL[c], marker=MK[c], ls="none", ms=4,
                      label=LBL[c]) for c in CONDS]
ax.legend(handles=handles, frameon=False, loc="lower right", ncols=2,
          handletextpad=0.2, columnspacing=0.8)
panel_letter(ax, "b")
save(fig, "fig4_direction")

print("all v2 figures done")
