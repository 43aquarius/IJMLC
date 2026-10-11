# Budget-Split Deep Ensembles vs. Snapshot Ensembles and Weight Averaging for Calibrated Uncertainty

Research artifacts for the manuscript ***"Budget-split deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty"***, prepared for submission to the *International Journal of Machine Learning and Cybernetics* (IJMLC).

> **One-sentence summary.** Under an identical training budget of 60 SGD epochs, splitting the budget across independently restarted networks (budget-split deep ensembles) yields better-calibrated uncertainty than extending single-model training, cycling the learning rate to harvest snapshots, or averaging the weights of those snapshots — and it is the only tested strategy that improves out-of-distribution detection.

---

## 1. Research Question

Practitioners deploying classifiers usually face a **fixed training-compute budget**, yet most method comparisons assume unconstrained budgets. This study asks: *given a fixed budget, how should it be spent to obtain the best-calibrated predictive uncertainty?*

## 2. Methods Summary

Under an identical total budget of **60 SGD epochs**, four allocation strategies were compared for an MLP (784–128–64–10, ~110k parameters, ReLU, no Dropout/BN) trained on **Fashion-MNIST** (in-distribution) with **MNIST** as an out-of-distribution probe:

| Strategy | Budget allocation | Combination rule |
|---|---|---|
| **Single** | 1 model × 60 epochs | — |
| **DeepEns** (budget-split) | 3 models × 20 epochs, independent restarts | prediction averaging |
| **Snapshot** | 1 run × 60 epochs, 3 cyclic-LR cycles | prediction averaging of 3 cycle-end snapshots |
| **SWA** | same 3 checkpoints as Snapshot | uniform weight averaging |

Shared training configuration: SGD, batch 256, momentum 0.9, weight decay 1e-4; 54,000 train / 6,000 validation / official 10,000-image test split; **10 seeded replications** per condition. The first ensemble member of every condition is bit-identical across conditions (verified), so all comparisons are fully budget-matched and paired at the seed level.

An exploratory variant (**SWA-dense**, averaging all checkpoints from epochs 21–60) is reported separately in the supplementary material.

## 3. Key Results (10 seeds, mean values)

| Metric (test) | Single | DeepEns | Snapshot | SWA |
|---|---:|---:|---:|---:|
| NLL ↓ | 0.5265 | **0.3020** | 0.3485 | 0.3868 |
| Accuracy ↑ | 0.8895 | **0.8965** | 0.8935 | 0.8926 |
| Brier ↓ | 0.1796 | **0.1504** | 0.1596 | 0.1646 |
| ECE-15 ↓ | 0.0702 | **0.0236** | 0.0444 | 0.0517 |
| OOD AUROC (MSP) ↑ | 0.7533 | **0.8502** | 0.7956 | 0.7504 |

- Every strategy improves NLL over Single (DeepEns −0.225, 95% CI [−0.236, −0.213]; Holm-adjusted exact permutation *P* = 0.0098 per comparison).
- Ordering **DeepEns > Snapshot > SWA > Single** replicates across calibration and OOD metrics.
- **Only prediction averaging improves OOD detection**; SWA shows no evidence of OOD improvement (ΔAUROC = −0.003, 95% CI [−0.017, +0.011], *P* = 0.64).
- Mechanism (member-level measurements): budget-split restarts combine **higher member calibration** (member NLL 0.338 vs. 0.404) **and higher between-member diversity** (JSD 0.0150 vs. 0.0106) relative to snapshots.

**Scope of evidence.** All conclusions are bounded to small networks, one dataset family, and one shift type; see the paper's Limitations section.

## 4. Repository Structure

```
.
├── paper/                  # Final manuscript PDF (also attached to the GitHub Release)
├── manuscript-source/     # LaTeX source (main.tex) + cover page source
├── code/                  # All experiment / analysis / figure scripts (Python)
│   ├── run_experiments.py      # main budget-matched experiment (4 conditions × 10 seeds)
│   ├── run_swa_dense.py        # exploratory SWA-dense variant
│   ├── analyze_results.py      # statistics: paired contrasts, permutation tests, Holm
│   ├── make_figures.py         # all figures from source data
│   ├── verify_seed0.py         # bit-level reproducibility check of shared first member
│   └── ...
├── results/                # Raw per-seed results (JSONL), analysis outputs, summaries
├── figures/                # Final figures (PDF + PNG)
├── source-data/            # Per-panel CSV source data for every figure
└── research-docs/          # Pre-registered design, claim–evidence map, figure contract, review report
```

## 5. Reproducing the Experiments

Requirements: Python 3.10+ with CPU-only PyTorch (`pip install -r code/requirements.txt`); no GPU needed.

```bash
cd code
python download_data.py      # downloads Fashion-MNIST + MNIST
python run_experiments.py    # ~4-6 h on 2 CPU cores; 4 conditions × 10 seeds
python run_swa_dense.py      # exploratory dense-averaging variant
python analyze_results.py    # paired contrasts, exact permutation tests, Holm correction
python make_figures.py       # regenerates all figures from results
python verify_seed0.py       # bit-level determinism check (shared first member)
```

Every reported number can be traced: `results/experiment.jsonl` holds per-seed, per-member raw metrics; `results/analysis.json` holds all statistical tests; `source-data/*.csv` holds the exact values behind each figure panel. A full determinism audit (24/24 metrics exact-match re-run) is documented in `research-docs/research-design.md`.

## 6. Research-Integrity Notes

- **No fabricated results.** All numbers in the paper come from the committed raw result files; figures are generated from committed per-panel CSVs.
- **Statistical rigor.** Seed is the unit of replication; contrasts are seed-paired; exact sign-flip permutation tests with Holm correction over the primary family; exploratory analyses are labeled as such.
- **AI involvement.** This research workflow, including code, analysis, and manuscript drafting, was conducted with AI assistance (Qinyan Nature Skills workflow); authorship and affiliations are pending author confirmation. See the manuscript title block.
- **Scope honesty.** Claims are limited to the studied regime (small MLP, Fashion-MNIST/MNIST, one budget level, ensemble size 3).

## 7. Citation

Preprint, 2026. If you use this work, please cite the paper release:

```bibtex
@misc{budgetsplit2026,
  title  = {Budget-split deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty},
  author = {43aquarius},
  year   = {2026},
  note   = {Preprint, prepared for the International Journal of Machine Learning and Cybernetics},
  url    = {https://github.com/43aquarius/IJMLC}
}
```

## 8. License

Code and data artifacts in this repository are provided for research and reproducibility purposes. The manuscript is a preprint under revision; reuse rights will be determined by the final publication agreement.
