# Budget-Split Deep Ensembles vs. Snapshot Ensembles and Weight Averaging for Calibrated Uncertainty

Research artifacts for the manuscript ***"Budget-split deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty"*** (v2, prepared for the *International Journal of Machine Learning and Cybernetics*).

**Author:** Chang Tan (Dalian University of Technology) — corresponding: aquars43@foxmail.com

> **One-sentence summary.** Under an identical training budget, splitting the budget across independently restarted networks (budget-split deep ensembles) yields better-calibrated uncertainty than extending single-model training, cycling the learning rate to harvest snapshots, or averaging the weights of those snapshots — an ordering that is robust across budgets, ensemble sizes and dataset directions, survives per-condition temperature scaling, and extends to out-of-distribution detection, where only prediction averaging helps.

---

## 1. Research Question

Practitioners who need calibrated predictive uncertainty usually face a **fixed training budget**, yet method comparisons typically let every method train until it stops improving. This study asks: *given a fixed budget, how should it be spent?*

## 2. Design

Under an identical total budget of **B SGD epochs**, four allocation strategies are compared for an MLP (784–128–64–10, ~110k parameters, ReLU, no Dropout/BN) trained with SGD (batch 256, momentum 0.9, weight decay 1e-4), 54,000 train / 6,000 validation / official test split, **10 seeded replications** per setting:

| Strategy | Allocation | Combination |
|---|---|---|
| **Single** | 1 model × B epochs | — |
| **DeepEns** (budget-split) | k models × B/k epochs, independent restarts | prediction averaging |
| **Snapshot** | 1 run × B epochs, k cyclic-LR cycles | prediction averaging of k cycle-end snapshots |
| **SWA** | the same k checkpoints | uniform weight averaging |

Clean-by-construction contrasts: the first DeepEns member is bit-identical to the first cyclic snapshot (verified), and Snapshot vs. SWA combine the *identical* checkpoints, isolating function-space vs. parameter-space averaging.

## 3. Settings and Key Results (10 seeds each, Holm-adjusted exact permutation tests)

| Setting | Single NLL | DeepEns NLL | Snapshot NLL | SWA NLL | Notes |
|---|---:|---:|---:|---:|---|
| **Fashion-MNIST, B=60, k=3** (core) | 0.5265 | **0.3020** | 0.3485 | 0.3868 | all contrasts p=0.0098; after per-condition TS: 0.3325 / **0.2891** / 0.3012 / 0.3104 |
| Fashion-MNIST, B=30, k=3 | 0.3795 | **0.3041** | 0.3124 | 0.3265 | low budget: gaps compress |
| Fashion-MNIST, B=120, k=3 | 0.6672 | **0.3355** | 0.4389 | 0.5120 | budget-split advantage **grows** with budget |
| Fashion-MNIST, B=60, k=5 | 0.5265 | **0.2974** | 0.3230 | 0.3592 | all strategies improve with k |
| **MNIST, B=60, k=3** (reversed) | 0.0724 | **0.0565** | 0.0709 | 0.0741 | boundary condition: only DeepEns separates from Single (p=0.0098 vs p=0.41) |

- **OOD detection (MSP AUROC):** DeepEns is the only strategy that improves detection on all four in-distribution→probe combinations (Fashion-MNIST→MNIST +0.097, →KMNIST +0.110; MNIST→Fashion-MNIST +0.014, →KMNIST +0.024); SWA shows no reliable improvement on any combination (core MNIST probe: −0.003, p=0.64).
- **Temperature scaling** (fitted per condition on validation): repairs much of every condition's miscalibration (Single 0.527→0.333) but leaves DeepEns significantly best in every setting, and changes OOD AUROC by at most +0.012.
- **Mechanism:** budget-split members are better calibrated (member NLL 0.338 vs 0.404) *and* more diverse (JSD 0.0150 vs 0.0106) than continued-training snapshots.

**Scope.** Small MLPs, grayscale 28×28 image tasks, two dataset directions, epoch-denominated budgets, k ∈ {3,5}; see the paper's Limitations section.

## 4. Repository Structure

```
├── paper/                       # Manuscript PDF (v2, IJMLC format; also on the Release)
├── manuscript-source/          # Complete LaTeX source (author-year citations)
├── code/
│   ├── run_experiments.py           # v1 core experiment (pre-registered)
│   ├── run_experiments_v2.py        # v2 extensions: budgets/sizes/direction/TS/KMNIST
│   ├── common.py                    # shared training + metrics + temperature scaling
│   ├── analyze_results.py           # v1 statistics
│   ├── analyze_v2.py                # v2 statistics (5 settings, TS families)
│   ├── make_figures.py / make_figures_v2.py
│   └── ...
├── results/
│   ├── experiment.jsonl             # v1 raw per-seed records (core setting)
│   ├── v2/                          # v2 raw per-seed records × 5 settings + analysis
│   └── analysis.json, contrasts.csv, ...
├── figures/                     # 4 main + 4 supplementary figures (PDF + PNG)
├── source-data/                 # Per-panel CSV source data for every figure
└── research-docs/               # Design, audit, literature review, experiment plan,
                                 # revision log, claim–evidence maps, submission checklist
```

## 5. Reproducing

```bash
cd code
pip install -r requirements.txt          # CPU-only PyTorch
python download_data.py                  # Fashion-MNIST + MNIST
python download_data_v2.py               # adds KMNIST (datasets_v2.npz)
python run_experiments.py                # v1 core (optional; v2 re-verifies it)
python run_experiments_v2.py --id fmnist --budget 60 --k 3 --seeds 0:10 \
    --out ../results/v2/experiment_v2_fmnist_B60_k3.jsonl
# ... and the other settings (--id mnist, --budget 30/120, --k 5)
python analyze_v2.py                     # all statistics
python make_figures.py && python make_figures_v2.py
```

The v2 pipeline **reproduces v1 bit-for-bit** (seed-0 re-run: 28/28 recorded metrics exact match), which serves as the release's determinism gate.

## 6. Research-Integrity Notes

- **No fabricated results.** Every number traces to committed raw JSONL records; figures regenerate from committed per-panel CSVs.
- **Statistical rigor.** Seed is the unit of replication; paired contrasts; exact sign-flip permutation tests; Holm correction per pre-specified family; extensions labelled as non-preregistered.
- **AI involvement.** Code, analysis and drafting were produced with AI assistance (Qinyan Nature Skills workflow) under the author's direction; all numbers were verified against the released records. See the manuscript's Declarations.
- **Honest scope.** Conclusions are bounded to the studied regime; the saturated-task boundary condition (MNIST) is reported prominently, not hidden.

## 7. Citation

```bibtex
@article{tan2026budgetsplit,
  title   = {Budget-split deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty},
  author  = {Tan, Chang},
  journal = {Preprint, prepared for the International Journal of Machine Learning and Cybernetics},
  year    = {2026},
  url     = {https://github.com/43aquarius/IJMLC}
}
```

## 8. Version History

- **v2.0.0 (11 Oct 2026):** IJMLC-format rewrite; adds budget sweep (30/120), ensemble size k=5, reversed MNIST direction, KMNIST second OOD probe, per-condition temperature scaling; author-year citations; Declarations incl. AI-use disclosure.
- **v1.0.0 (22 Sep 2026):** pre-registered core experiment (Fashion-MNIST, B=60, k=3, 10 seeds) with SWA-dense exploratory variant. Available under the `paper-v1.0.0` release tag.

## 9. License

Code and data artifacts are provided for research and reproducibility purposes. The manuscript is a preprint under revision; reuse rights will be determined by the final publication agreement.
