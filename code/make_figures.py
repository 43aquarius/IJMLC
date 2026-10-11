#!/usr/bin/env python3
"""Render all figures per paper/figure-contract.md.

Style: Okabe-Ito colour-blind-safe palette, Liberation Sans (Arial-metric),
vector PDF primary export + 600 dpi PNG preview, 183 mm main / 120 mm suppl.
All seed-level observations are shown (no aggregate-only displays).
"""
import json

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
    "font.size": 7.5,
    "axes.linewidth": 0.6,
    "axes.labelsize": 7.5,
    "axes.titlesize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 6.5,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

D = json.load(open("/home/z/my-project/results/figure_data.json"))
FIGDIR = "/home/z/my-project/figures"
SDIR = f"{FIGDIR}/source_data"

# Okabe-Ito
COL = {"single": "#999999", "deepens": "#0072B2", "snapshot": "#E69F00",
       "swa": "#009E73", "swa_dense": "#CC79A7"}
MK = {"single": "o", "deepens": "s", "snapshot": "D", "swa": "^", "swa_dense": "v"}
LBL = {"single": "Single", "deepens": "DeepEns", "snapshot": "Snapshot",
       "swa": "SWA", "swa_dense": "SWA-dense"}
CONDS = ["single", "deepens", "snapshot", "swa"]
COND_LBL = [LBL[c] for c in CONDS]


def save(fig, name, dpi=600):
    fig.savefig(f"{FIGDIR}/{name}.pdf")
    fig.savefig(f"{FIGDIR}/{name}.png", dpi=dpi)
    plt.close(fig)
    print(f"saved {name}.pdf/.png")


def panel_letter(ax, letter):
    ax.text(-0.16, 1.06, letter, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top", ha="left")


def paired_dot(ax, metric, ylabel, conds=CONDS, lbls=None, data=None, fmt="{:.3f}"):
    """Paired seed lines + condition means with distinct markers."""
    lbls = lbls or [LBL[c] for c in conds]
    data = data or {c: D[f"seeds_{metric}"][c] for c in conds}
    x = np.arange(len(conds))
    V = np.array([data[c] for c in conds], dtype=float)  # cond x seed
    for s in range(V.shape[1]):
        ax.plot(x, V[:, s], color="#BBBBBB", lw=0.5, alpha=0.7, zorder=1)
    for i, c in enumerate(conds):
        ax.scatter(np.full(V.shape[1], i), V[i], s=9, color=COL[c], marker=MK[c],
                   alpha=0.55, linewidths=0, zorder=2)
        ax.scatter([i], [V[i].mean()], s=46, color=COL[c], marker=MK[c],
                   edgecolor="black", linewidths=0.7, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(lbls, fontsize=6.8)
    ax.set_xlim(-0.45, len(conds) - 0.55)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", lw=0.35, color="#E6E6E6")
    ax.set_axisbelow(True)
    return V


# ============================================================================= Fig 1
fig = plt.figure(figsize=(7.2, 5.35), constrained_layout=True)
gs = fig.add_gridspec(2, 3, width_ratios=[1.12, 1.0, 1.0], height_ratios=[1, 1])

# --- a: LR schedules (real values used in training)
ax = fig.add_subplot(gs[0, 0])
ep = np.linspace(0, 60, 601)
cos_single = 0.05 * (1 + np.cos(np.pi * ep / 60))
cos_cycle = 0.05 * (1 + np.cos(np.pi * (ep % 20) / 20))
ax.plot(ep, cos_single, color=COL["single"], lw=1.3, label="Single: one 60-epoch cosine")
ax.plot(ep, cos_cycle, color=COL["snapshot"], lw=1.3, ls="--",
        label="Cyclic run: 3 cosine cycles")
for i, xe in enumerate([20, 40, 60]):
    ax.plot([xe], [0.0], marker="D", ms=5.5, color="#444444", zorder=5, ls="none")
    ax.annotate(f"$\\theta_{{{i+1}}}$", (xe, 0.0), xytext=(xe - 4.2, 0.018),
                fontsize=7.5, color="#444444")
# DeepEns member schedule: one 20-epoch cosine, shown offset above for clarity
seg = np.linspace(0, 20, 200)
ax.plot(seg, 0.05 * (1 + np.cos(np.pi * seg / 20)) + 0.11, color=COL["deepens"],
        lw=1.3, ls=":", alpha=0.9)
ax.text(22, 0.170, "DeepEns: three independent\nruns of this short cosine\n(shown offset)",
        fontsize=6.0, color=COL["deepens"], ha="left", va="top")
ax.set_ylim(-0.015, 0.225)
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_xlabel("Training epoch (budget axis)")
ax.set_ylabel("Learning rate")
ax.legend(loc="center left", bbox_to_anchor=(0.015, 0.42), frameon=False,
          handlelength=1.5, borderaxespad=0.0, labelspacing=0.3)
panel_letter(ax, "a")

# --- b: test NLL
ax = fig.add_subplot(gs[0, 1])
V = paired_dot(ax, "nll", "Test NLL")
for i, c in enumerate(CONDS):
    ax.annotate(f"{V[i].mean():.3f}", (i, V[i].mean()), xytext=(0, 6),
                textcoords="offset points", fontsize=6.3, ha="center", color=COL[c])
ax.set_title("Predictive negative log-likelihood (lower is better)", fontsize=6.8, pad=3)
panel_letter(ax, "b")

# --- c: reliability diagrams
ax = fig.add_subplot(gs[0, 2])
for c in CONDS:
    r = D["reliability"][c]
    cnf = [v for v in r["bin_conf"] if v is not None]
    acc = [v for v, cc in zip(r["bin_acc"], r["bin_conf"]) if cc is not None]
    ax.plot(cnf, acc, color=COL[c], marker=MK[c], ms=2.6, lw=1.1,
            label=LBL[c], alpha=0.95)
ax.plot([0, 1], [0, 1], color="black", lw=0.7, ls="-", alpha=0.6)
ax.set_xlabel("Predicted confidence")
ax.set_ylabel("Empirical accuracy")
ax.set_xlim(0.3, 1.0)
ax.set_ylim(0.3, 1.0)
ax.set_aspect("equal")
ax.legend(loc="upper left", frameon=False, borderaxespad=0.2, handlelength=1.4,
          labelspacing=0.25)
ax.text(0.97, 0.30, "diagonal:\nperfect calibration", fontsize=6.0, ha="right",
        color="#444444")
ax.set_title("Calibration (15 equal-width bins)", fontsize=6.8, pad=3)
panel_letter(ax, "c")

# --- d: OOD AUROC (MSP)
ax = fig.add_subplot(gs[1, 0])
V = paired_dot(ax, "auroc_msp", "OOD detection AUROC (MSP)")
for i, c in enumerate(CONDS):
    ax.annotate(f"{V[i].mean():.3f}", (i, V[i].mean()), xytext=(0, 6),
                textcoords="offset points", fontsize=6.3, ha="center", color=COL[c])
ax.axhline(0.5, color="#888888", lw=0.6, ls=":")
ax.text(0.02, 0.505, "chance", fontsize=6.0, color="#888888")
ax.set_title("MNIST probe (in-distribution: Fashion-MNIST)", fontsize=6.8, pad=3)
panel_letter(ax, "d")

# --- e: mechanism: member NLL + diversity
ax = fig.add_subplot(gs[1, 1])
paired_dot(ax, "member_mean_nll", "Member mean NLL", conds=["deepens", "snapshot"],
           lbls=["DeepEns-3\nmembers", "Snapshot-3\nmembers"])
panel_letter(ax, "e")
ax2 = fig.add_subplot(gs[1, 2])
paired_dot(ax, "disagreement_jsd", "Ensemble disagreement (JSD)",
           conds=["deepens", "snapshot"],
           lbls=["DeepEns-3", "Snapshot-3"])
panel_letter(ax2, "f")
ax.set_title("Members individually", fontsize=6.8, pad=3)
ax2.set_title("Between-member diversity", fontsize=6.8, pad=3)

save(fig, "fig1_main")

# ============================================================================= Suppl 1
fig, axes = plt.subplots(2, 4, figsize=(7.2, 3.5), constrained_layout=True)
for j, c in enumerate(CONDS):
    ax = axes[0, j]
    r = D["reliability"][c]
    for sa, sc in zip(r["per_seed_acc"], r["per_seed_conf"]):
        cnf = [v for v in sc if v is not None]
        acc = [v for v, cc in zip(sa, sc) if cc is not None]
        ax.plot(cnf, acc, color=COL[c], lw=0.5, alpha=0.45)
    cnf = [v for v in r["bin_conf"] if v is not None]
    acc = [v for v, cc in zip(r["bin_acc"], r["bin_conf"]) if cc is not None]
    ax.plot(cnf, acc, color=COL[c], lw=1.4)
    ax.plot([0, 1], [0, 1], color="black", lw=0.6, alpha=0.6)
    ax.set_xlim(0.3, 1); ax.set_ylim(0.3, 1)
    ax.set_title(LBL[c], fontsize=7)
    if j == 0:
        ax.set_ylabel("Accuracy")
    ax.set_xlabel("Confidence")
    # ECE in corner
    ece_v = np.mean(D["seeds_ece15"][c])
    ax.text(0.95, 0.36, f"ECE {ece_v:.3f}", fontsize=6.3, ha="right", color="#333333")
for j in range(4):
    axes[1, j].set_visible(False)
fig.get_layout_engine().set(h_pad=0.1)
save(fig, "suppl_fig1_reliability")

# ============================================================================= Suppl 2
fig, axes = plt.subplots(1, 4, figsize=(7.2, 1.95), constrained_layout=True)
for j, c in enumerate(CONDS):
    ax = axes[j]
    h = D["msp_histograms"][c]
    ec = np.array(h["edges"])
    w = ec[1] - ec[0]
    ax.bar(ec[:-1] + w / 2, h["density_in"], width=w * 0.96, color=COL[c],
           alpha=0.95, label="in-dist. (Fashion)")
    ax.bar(ec[:-1] + w / 2, h["density_out"], width=w * 0.96, color="#333333",
           alpha=0.45, label="OOD (MNIST)")
    ax.set_title(LBL[c], fontsize=7)
    ax.set_xlabel("Max-softmax score")
    if j == 0:
        ax.set_ylabel("Density")
        ax.legend(frameon=False, fontsize=6.0, loc="upper left")
save(fig, "suppl_fig2_msp_hist")

# ============================================================================= Suppl 3: SWA-dense
fig, axes = plt.subplots(1, 2, figsize=(4.7, 2.3), constrained_layout=True)
conds5 = CONDS + ["swa_dense"]
data_nll = {c: D["seeds_nll"][c] for c in CONDS}
data_nll["swa_dense"] = D["seeds_swa_dense"]["nll"]
data_auc = {c: D["seeds_auroc_msp"][c] for c in CONDS}
data_auc["swa_dense"] = D["seeds_swa_dense"]["auroc_msp"]
paired_dot(axes[0], "nll", "Test NLL", conds=conds5,
           lbls=[LBL[c] for c in conds5], data=data_nll)
axes[0].set_title("NLL", fontsize=7)
paired_dot(axes[1], "auroc_msp", "AUROC (MSP)", conds=conds5,
            lbls=[LBL[c] for c in conds5], data=data_auc)
axes[1].set_title("OOD AUROC", fontsize=7)
axes[1].tick_params(axis="x", labelrotation=30)
for ax, letter in zip(axes, ["a", "b"]):
    ax.text(-0.28, 1.12, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top")
save(fig, "suppl_fig3_swa_dense")

# ============================================================================= Suppl 4: learning curves
fig, ax = plt.subplots(figsize=(3.5, 2.6), constrained_layout=True)
for name, col, lab in [("single", COL["single"], "Single (long cosine)"),
                       ("cyclic", COL["snapshot"], "Cyclic (3 cycles)")]:
    lc = D["learning_curves"][name]
    m = np.array(lc["mean"]); s = np.array(lc["sd"]); e = np.array(lc["epochs"])
    ax.plot(e, m, color=col, lw=1.2, label=lab)
    ax.fill_between(e, m - s, m + s, color=col, alpha=0.18, lw=0)
for xe in [20, 40]:
    ax.axvline(xe, color="#888888", lw=0.6, ls=":")
ax.text(20, ax.get_ylim()[1] * 0.98, " cycle end", fontsize=6.0, va="top", color="#666666")
ax.set_xlabel("Training epoch")
ax.set_ylabel("Validation NLL (6,000 held-out)")
ax.legend(frameon=False, loc="upper right")
save(fig, "suppl_fig4_curves")

# ============================================================================= source data
import csv, os
os.makedirs(SDIR, exist_ok=True)
seeds = list(range(10))
with open(f"{SDIR}/fig1b_nll.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seed"] + CONDS)
    for s in seeds:
        w.writerow([s] + [D["seeds_nll"][c][s] for c in CONDS])
with open(f"{SDIR}/fig1d_auroc.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seed"] + CONDS)
    for s in seeds:
        w.writerow([s] + [D["seeds_auroc_msp"][c][s] for c in CONDS])
with open(f"{SDIR}/fig1e_members.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seed", "deepens_member_nll", "snapshot_member_nll",
                "deepens_jsd", "snapshot_jsd"])
    for s in seeds:
        w.writerow([s, D["seeds_member_mean_nll"]["deepens"][s],
                     D["seeds_member_mean_nll"]["snapshot"][s],
                     D["seeds_disagreement_jsd"]["deepens"][s],
                     D["seeds_disagreement_jsd"]["snapshot"][s]])
with open(f"{SDIR}/fig1c_reliability.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["condition", "bin", "bin_conf_mean", "bin_acc_mean", "bin_count_mean"])
    for c in CONDS:
        r = D["reliability"][c]
        for b in range(15):
            w.writerow([c, b, r["bin_conf"][b], r["bin_acc"][b], r["bin_count"][b]])
with open(f"{SDIR}/fig1a_lr_schedule.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["epoch", "single_cosine", "cyclic_cosine", "deepens_member_cosine"])
    for i, e in enumerate(ep[::6]):
        w.writerow([round(e, 1), round(cos_single[::6][i], 6),
                    round(cos_cycle[::6][i], 6),
                    round(0.05 * (1 + np.cos(np.pi * ((e % 20) / 20))), 6)])
with open(f"{SDIR}/suppl3_swa_dense.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seed", "nll", "acc", "ece15", "auroc_msp"])
    for s in seeds:
        d = D["seeds_swa_dense"]
        w.writerow([s, d["nll"][s], d["acc"][s], d["ece15"][s], d["auroc_msp"][s]])
with open(f"{SDIR}/suppl4_curves.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["epoch", "single_mean", "single_sd", "cyclic_mean", "cyclic_sd"])
    lc1 = D["learning_curves"]["single"]; lc2 = D["learning_curves"]["cyclic"]
    for i in range(60):
        w.writerow([i + 1, lc1["mean"][i], lc1["sd"][i], lc2["mean"][i], lc2["sd"][i]])
print("source data CSVs written to", SDIR)
