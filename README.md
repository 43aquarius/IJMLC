# Deep Ensembles vs. Snapshot Ensembles and Weight Averaging for Calibrated Uncertainty under Fixed Training Budgets

Research artifacts for the manuscript ***"Deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty under fixed training budgets"*** (v4.1.2, prepared for the *International Journal of Machine Learning and Cybernetics*).

**Author:** Chang Tan (Dalian University of Technology) — corresponding: aquars43@foxmail.com

> **One-sentence summary.** Under an identical training budget, splitting the budget across independently restarted networks (budget-split deep ensembles) yields better-calibrated uncertainty than extending single-model training, cycling the learning rate to harvest snapshots, or averaging the weights of those snapshots — the four-way ordering holds on test NLL across budgets, ensemble sizes and (post-hoc) a convolutional architecture on CIFAR-10, survives per-condition temperature scaling at the core budget and above, and carries to out-of-distribution detection, where prediction averaging gives the largest and most consistent gains while weight averaging's smaller effects are task-dependent (on the near-saturated MNIST task only the budget-split ensemble separates from the single network; the CIFAR DeepEns–Snapshot advantage in calibration error is directionally consistent but not statistically resolved at n=10).

> **The manuscript itself — compiled PDF and LaTeX source — lives in the
> [releases](https://github.com/43aquarius/deep-ensembles-fixed-budget/releases)
> only**; this repository carries the code, data, figures and research
> trail that support the paper.

---

## 1. Research Question

Practitioners who need calibrated predictive uncertainty usually face a **fixed training budget**, yet method comparisons typically let every method train until it stops improving. This study asks: *given a fixed budget, how should it be spent?*

## 2. Design

Under an identical total budget of **B SGD epochs**, four allocation strategies are compared for an MLP (784–128–64–10, ~110k parameters, ReLU, no Dropout/BN; a ~34k-parameter CNN in the CIFAR extension) trained with SGD (batch 256, momentum 0.9, weight decay 1e-4), fixed train/validation splits, **10 seeded replications** per setting:

| Strategy | Allocation | Combination |
|---|---|---|
| **Single** | 1 model × B epochs | — |
| **DeepEns** (budget-split) | k models × B/k epochs, independent restarts | prediction averaging |
| **Snapshot** | 1 run × B epochs, k cyclic-LR cycles | prediction averaging of k cycle-end snapshots |
| **SWA** | the same k checkpoints | uniform weight averaging |

Clean-by-construction contrasts: the first DeepEns member is bit-identical to the first cyclic snapshot (verified in every setting), and Snapshot vs. SWA combine the *identical* checkpoints, so their contrast measures function-space vs. parameter-space averaging of the same weights.

## 3. Settings and Key Results (10 seeds each, Holm-adjusted exact permutation tests)

| Setting | Single NLL | DeepEns NLL | Snapshot NLL | SWA NLL | Notes |
|---|---:|---:|---:|---:|---|
| **Fashion-MNIST, B=60, k=3** (core, pre-registered) | 0.5265 | **0.3020** | 0.3485 | 0.3868 | all contrasts p=0.0098; after per-condition TS: 0.3325 / **0.2891** / 0.3012 / 0.3104 |
| Fashion-MNIST, B=30, k=3 | 0.3795 | **0.3041** | 0.3124 | 0.3265 | low budget: gaps compress; after TS the ensembles are statistically indistinguishable |
| Fashion-MNIST, B=120, k=3 | 0.6672 | **0.3355** | 0.4389 | 0.5120 | budget-split advantage **grows** with budget |
| Fashion-MNIST, B=60, k=5 | 0.5265 | **0.2974** | 0.3230 | 0.3592 | all strategies improve with k |
| **MNIST, B=60, k=3** (reversed) | 0.0724 | **0.0565** | 0.0709 | 0.0741 | boundary condition: only DeepEns separates from Single (p=0.0098 vs p=0.41); DeepEns beats SWA directly too (−0.0176, p=0.0020) |
| **CIFAR-10, B=60, k=3, small CNN** (post-hoc) | ~2.0 | **~0.69** | ~0.90 | ~1.08 | full replication with much larger margins; see `results/cifar/` |

(The CIFAR row's exact values, CIs and tests are in `results/cifar/analysis_cifar.json`; the manuscript's Table 4 reports them in full.)

- **OOD detection (MSP AUROC):** DeepEns improves detection on every one of the eleven setting→probe combinations (per-probe Holm-adjusted P ≤ 0.032; e.g. core Fashion-MNIST→MNIST +0.097, →KMNIST +0.110; CIFAR-100 +0.069); Snapshot on 9/11; SWA's effects are smaller and task-dependent (−0.016 to +0.025: significantly positive on 5 combinations incl. CIFAR-100 +0.025, significantly negative on one at B=120, null elsewhere). Full table: paper Supplementary Table S4 / `research-docs/ood-ts-statistics-v4.md`.
- **Temperature scaling** (fitted per condition on validation): repairs much of every condition's miscalibration (Single 0.527→0.333) but leaves DeepEns significantly best at the core budget and above; it shifts OOD AUROC by at most +0.012 on the digit tasks and up to +0.026 on CIFAR-10 (TS is not rank-preserving across samples in general; adaptive TS has even been used to improve OOD detection — Krumpl et al., WACV 2024); at B=30 it largely equalises the ensemble strategies.
- **Mechanism:** budget-split members are better calibrated (member NLL 0.338 vs 0.404) *and* more diverse (JSD 0.0150 vs 0.0106) than continued-training snapshots; both replicate on CIFAR-10.
- **Inference cost is not matched** by design: prediction averaging costs k forward passes per query, Single/SWA cost one (see the paper's Methods §3.1).

**Scope.** Small networks (110k-param MLP, 34k-param CNN), small-scale image tasks, epoch-denominated budgets, k ∈ {3,5}; see the paper's Limitations section.

## 4. Repository Structure

```
├── code/
│   ├── paths.py                     # repo-root path resolution (no hard-coded paths)
│   ├── common.py / common_cifar.py   # shared training + metrics + temperature scaling
│   ├── download_data*.py            # MNIST-family + CIFAR data (public mirrors)
│   ├── run_experiments.py           # v1 core experiment (pre-registered)
│   ├── run_experiments_v2.py        # v2 extensions: budgets/sizes/direction/TS/KMNIST
│   ├── run_experiments_cifar.py     # v3 cross-architecture extension (checkpointed, sharded)
│   ├── analyze_results.py / analyze_v2.py / analyze_cifar.py
│   ├── reanalysis_v4.py / verify_v4_numbers.py / diagnose_seed8.py
│   ├── verify_v41_stage{1,2,3}.py   # v4.1 independent recomputation audit
│   └── requirements.txt
├── results/
│   ├── experiment.jsonl             # v1 raw per-seed records (core setting)
│   ├── v2/                          # v2 raw per-seed records × 5 settings + analysis
│   ├── cifar/                       # v3 CIFAR raw per-seed records + analysis
│   ├── v4/                          # v4 re-analysis + seed-8 diagnosis
│   └── analysis.json, contrasts.csv, ...
├── figures/                     # 5 main + 4 supplementary figures (PDF + PNG)
├── source-data/                 # Per-panel CSV source data for every figure
└── research-docs/               # Design, audits, literature reviews, experiment plans,
                                 # revision logs, claim–evidence maps, submission checklists
```

*(The manuscript for every version — PDF and LaTeX source — is published as
release assets, not tracked in the repository tree. Each release carries
the paper PDF plus a source archive containing the exact LaTeX file and the
figure PDFs it compiles against.)*

## 5. Reproducing (clean clone)

```bash
python -m venv venv && source venv/bin/activate
pip install torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r code/requirements.txt
python code/download_data.py             # Fashion-MNIST + MNIST -> results/data/datasets.npz
python code/download_data_v2.py          # adds KMNIST -> datasets_v2.npz (no torchvision needed)
python code/download_data_cifar.py       # CIFAR-10 + CIFAR-100 (HuggingFace parquet mirrors)
# v1 core (optional; the v2 pipeline re-verifies it bit-for-bit):
python code/run_experiments.py
# v2 extensions:
python code/run_experiments_v2.py --id fmnist --budget 60 --k 3 --seeds 0:10 \
    --out results/v2/experiment_v2_fmnist_B60_k3.jsonl
#   ... and the other settings (--id mnist, --budget 30/120, --k 5)
# v3 CIFAR extension (~3.5 h on 2 CPU cores; sharded + checkpointed, safe to re-run):
python code/run_experiments_cifar.py --budget 60 --k 3 --seeds 0:10 \
    --out results/cifar/experiment_cifar_B60_k3.jsonl
python code/analyze_v2.py && python code/analyze_cifar.py
python code/make_figures.py && python code/make_figures_v2.py && python code/make_figures_cifar.py
# v4.1 audit: independent recomputation of every manuscript number from the raw records
python code/verify_v41_stage1.py && python code/verify_v41_stage2.py && python code/verify_v41_stage3.py
```

All scripts resolve paths relative to the repository root (override with the
`BME_ROOT` environment variable to relocate data/figures elsewhere).

**Determinism gates (verified):**
- v2 pipeline reproduces v1 bit-for-bit (seed-0 re-run: 28/28 recorded metrics exact match).
- Clean-environment gate (fresh venv, fresh data download, fresh directory): seed-0 re-run matched **all 110 recorded metric values bit-for-bit**.
- CIFAR pipeline: interrupted-and-resumed training is bitwise identical to one-shot training; shared-first-member bit-identity verified.
- v4.1 audit: 232/241 automated number checks reproduce the manuscript exactly from the raw records; the 9 exceptions are documented dispositions (one corrected table row, two re-scoped claims, and reference notes) — see `research-docs/number-verification-v4.1.md`.

## 6. Research-Integrity Notes

- **No fabricated results.** Every number traces to committed raw JSONL records; figures regenerate from committed per-panel CSVs. The CIFAR experiment's hypotheses and analysis plan were fixed in writing before any test-set evaluation and are labelled post-hoc in the paper.
- **Statistical rigor.** Seed is the unit of replication; paired contrasts; exact sign-flip permutation tests; Holm correction per pre-specified family; extensions labelled as non-preregistered; the B=30 secondary-metric and TS exceptions are reported, not hidden.
- **AI involvement.** Code, analysis, drafting and revisions were produced with AI assistance (Qinyan Nature Skills workflow) under the author's direction; all numbers were verified against the released records. See the manuscript's Declarations.
- **Honest scope.** Conclusions are bounded to the studied regime; the saturated-task boundary condition (MNIST) is reported prominently, not hidden.

## 7. Citation

```bibtex
@article{tan2026budgetsplit,
  title   = {Deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty under fixed training budgets},
  author  = {Tan, Chang},
  journal = {Preprint, prepared for the International Journal of Machine Learning and Cybernetics},
  year    = {2026},
  url     = {https://github.com/43aquarius/deep-ensembles-fixed-budget}
}
```

## 8. Version History

- **v4.1.2 (15 Oct 2026):** submission-package finalisation — no experiment was added, re-run or modified, and no reported number, table, figure, statistic or bibliography entry was changed. The two "Use of large language models" declaration paragraphs (added in v4.1.1) were withdrawn at the author's decision for the submission version; the Statements and Declarations section carries the five standard paragraphs (Funding / Competing interests / Author contributions / Data availability / Code availability), with the author-contribution statement entered through the journal's submission system, which publishes the form version in place of any in-manuscript statement. Title-page date updated to 15 October 2026 (25 → 24 pp.). A word-multiset proof on the compiled PDFs shows the v4.1.1 → v4.1.2 text difference is exactly the two withdrawn paragraphs, their two headings, the date token and one page-number token; the references section is unchanged apart from a page-number token shifted by the page break. Submission package prepared alongside (cover letter and author-contributions statement, docx + pdf, and the LaTeX source zip). The Code-availability release pointer names this release (`paper-v4.1.2`), a token-only change verified against the previously compiled v4.1.2 PDF by reverse-substitution character-exact comparison; full details in `research-docs/revision-log-v4.1.2.md`.
- **v4.1.1 (14 Oct 2026):** final pre-submission pass — no experimental or numerical changes. Declarations retitled to "Statements and Declarations" and reorganised into the six standard paragraphs (Funding / Competing interests / Author contributions / Use of large language models / Data availability / Code availability) per the official submission guidelines (accessed 14 Oct 2026); a factual LLM-use paragraph added at the end of Methods §3.6 (Reproducibility); abstract trimmed from 249 to 236 source-level words (all ten required content elements retained, checked programmatically); Supplementary Fig. S3 (SWA-dense comparison) widened from 4.7 to 7.2 inches to clear the crowded x-axis method labels — plotted data, statistics and axis ranges unchanged; cover letter draft added (`research-docs/`). The repository was renamed **IJMLC → deep-ensembles-fixed-budget** and both in-manuscript URLs updated to the canonical location (PDF recompiled and verified: URL-only change; page count and all checks unchanged); the LaTeX source moved from the repository tree into the release asset archive, so the tree now carries supporting materials only.
- **v4.1.0 (14 Oct 2026):** submission-preparation audit and targeted revision. One table display error corrected (Table 1 KMNIST-probe s.d. row, inherited from v2); abstract and contribution claims re-scoped to match the statistical evidence (the four-way ordering does not hold on the MNIST direction, where SWA is nominally below Single; the CIFAR ECE advantage of DeepEns over Snapshot reported as unresolved at n=10); the "by adjacency" inference on MNIST replaced by a direct DeepEns−SWA contrast (−0.0176, p=0.0020); causal language tightened in four passages; positioning paragraph made internally consistent and re-dated (literature re-check through 14 Oct 2026) with three new verified references (Brigato & Iocchi 2021; Ramé et al. 2022 DiWA; Krumpl et al. 2024 ATS); abstract trimmed to the journal's 150–250-word limit (248); full independent number recomputation (232/241 checks; dispositions documented); research-docs: revision log, claim–evidence matrix, literature positioning, number-verification report, final submission checklist. Manuscript PDFs moved out of the repository tree into release assets.
- **v4.0.0 (13 Oct 2026):** final pre-submission audit and scope corrections. OOD claims rewritten from the categorical "only prediction averaging helps" to the comparative, heterogeneity-reporting form backed by a fully defined post-hoc multiplicity framework (per-probe Holm families + setting-level + global sensitivity; new Supplementary Table S4 with all eleven setting→probe combinations); temperature-scaling OOD claim corrected (digit tasks ≤ +0.012; CIFAR-10 up to +0.026; "ranking-invariant" theory statement removed); CIFAR DeepEns−Snapshot ECE contrast reported as directionally consistent but statistically unresolved (P=0.082); anomalous CIFAR replicate diagnosed (one fresh restart collapsed to uniform predictions in epoch 1 — deterministic re-run) and retained under the no-exclusion rule with leave-one-out sensitivity; `download_data_cifar.py` integrity-check float32 accumulation bug fixed (stored data verified correct in float64); v4 research documents (audit, claim–evidence matrix, OOD/TS statistics report, anomalous-seed report, revision log, submission checklist) and `results/v4/` independent re-analysis released.
- **v3.0.0 (12 Oct 2026):** cross-architecture replication on CIFAR-10 (small CNN, post-hoc-labelled); scope-corrected title and claims (NLL/ECE ordering; B=30 secondary-metric and TS exceptions reported); four-dimension cost accounting (training vs wall-clock vs inference vs deployment); 2024–2025 literature re-check with three new verified references; path-independent code (clean-clone reproduction gate: 110/110 bit-identical); torchvision-free data pipeline.
- **v2.0.0 (11 Oct 2026):** IJMLC-format rewrite; adds budget sweep (30/120), ensemble size k=5, reversed MNIST direction, KMNIST second OOD probe, per-condition temperature scaling; author-year citations; Declarations incl. AI-use disclosure.
- **v1.0.0 (22 Sep 2026):** pre-registered core experiment (Fashion-MNIST, B=60, k=3, 10 seeds) with SWA-dense exploratory variant. Available under the `paper-v1.0.0` release tag.

## 9. License

Code and data artifacts are provided for research and reproducibility purposes. The manuscript is a preprint under revision; reuse rights will be determined by the final publication agreement.
