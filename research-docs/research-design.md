# Statistical Analysis Plan (Pre-registered)

**Study**: Budget-matched comparison of ensemble strategies for predictive uncertainty
**Mode**: qinyan-nature-statistics `plan` (written before any test-set evaluation)
**Date**: 2026-09-22

## 1. Scientific question and estimand

**Question.** Under a fixed total training-compute budget (B epochs of SGD), how should the budget be allocated to obtain accurate and well-calibrated predictive uncertainty: (i) one model trained for the full budget, (ii) an ensemble of k independently initialized models trained B/k epochs each, (iii) a snapshot ensemble collected from a single cyclic-learning-rate run of B epochs, or (iv) the weight average (SWA) of the same cyclic-run snapshots?

**Estimands.** For each metric M in {NLL, accuracy, Brier score, ECE, OOD AUROC} and each condition c in {DeepEns, Snapshot, SWA}, the estimand is the mean paired difference
ΔM_c = E_s[ M_{s,c} − M_{s,Single} ],
where s indexes independent experimental replicates (seeds). The primary estimand is ΔNLL (test negative log-likelihood); all other metrics are secondary. A fifth contrast, ΔM_{Snapshot−SWA} (same training trajectory, different combination rule) isolates the combination mechanism.

**Target population.** The specific regime studied: small multilayer perceptrons (≈110k parameters) trained with SGD on 28×28 grayscale image classification (Fashion-MNIST), evaluated in-distribution and under a dataset-shift OOD probe (MNIST). Extrapolation beyond this regime is out of scope.

## 2. Experimental units, n, and design hierarchy

- **Independent experimental unit**: one seed = one full independent replication of the entire experiment (all four conditions freshly initialized and trained under that seed). **n = 10 seeds** (amended 2026-09-22 after pilot timing calibration but before any test-set evaluation; original plan n = 5; the amendment only increases replication and cannot bias results, as no outcome data had been observed).
- Observations within a seed (test samples, ensemble members, snapshots) are **not** independent units; they are summarized to one number per (seed, condition, metric) before inference.
- All contrasts are **within-seed paired** (every condition is run under every seed).
- Snapshot and SWA conditions are derived from the **same** training run within a seed (identical trajectory and checkpoints); their contrast therefore has no run-to-run noise, only the deterministic difference between prediction-averaging and weight-averaging.
- **Shared first member (compute accounting + variance control).** Within a seed, the first 20 epochs of the cyclic run (with its first cycle annealed over exactly 20 epochs, same initialization and data order as an independent run) are bit-identical to a fresh 20-epoch fully annealed run; this checkpoint is therefore used both as Snapshot member 1 and as DeepEns member 1. This sharing is a property of the experiment implementation (verified programmatically), not of the recipes: DeepEns-3 as a standalone recipe remains three independent 20-epoch runs, and Snapshot-3 remains one 60-epoch cyclic run. Total compute per seed: 160 training epochs.

## 3. Design (all conditions consume the identical budget B = 60 epochs of training compute)

| Condition | Runs | Epochs each | LR schedule | Combination at prediction |
|---|---|---|---|---|
| Single | 1 | 60 | cosine 0.1→0 over 60 | final weights |
| DeepEns-3 | 3 | 20 | cosine 0.1→0 over 20 | mean softmax over 3 members |
| Snapshot-3 | 1 | 60 | cosine 0.1→0, 3 cycles of 20 | mean softmax over 3 cycle-end snapshots |
| SWA-3 | 1 (= same run as Snapshot) | 60 | identical cyclic schedule | uniform weight average of the 3 cycle-end snapshots |

Fixed elements shared by all conditions: architecture MLP 784–128–64–10 (ReLU, no dropout, no batch norm), SGD momentum 0.9, weight decay 1e-4, batch size 256, identical data split and normalization, identical number of gradient steps per epoch (211), seeds derived deterministically from (replicate, condition, member).

**Data splits.** Fashion-MNIST: 54,000 train / 6,000 validation / 10,000 test. Validation is used only for monitoring and learning curves; no early stopping, no model or hyperparameter selection on validation or test. OOD probe: MNIST test set (10,000 images). Hyperparameters (LR 0.1, momentum, weight decay, B = 60, k = 3) were fixed from common literature practice before the first test-set evaluation; any change forced by pilot divergence would be based on training loss only and documented.

## 4. Outcomes and metrics

Primary outcome: **test NLL** of the predictive distribution (ensemble mean probability where applicable).
Secondary outcomes: test accuracy; Brier score; ECE (15 equal-width bins); OOD AUROC using the maximum-softmax-probability score (MNIST test as OOD); ensemble member disagreement (mean pairwise Jensen–Shannon divergence between member predictive distributions, descriptive only).

## 5. Analysis specification

1. For each (seed, condition): compute metrics on the untouched test set. Per-condition summary: mean across seeds ± s.d., and all five individual seed values displayed.
2. Paired differences vs Single (and Snapshot−SWA): mean Δ, two-sided 95% t-CI (n−1 = 4 df), and an exact paired sign-flip permutation p-value (2^5 = 32 sign patterns, exact enumeration).
3. **Multiplicity**: Holm–Bonferroni correction across the five pre-specified contrasts on the primary outcome (NLL) only; secondary metrics are reported as effect estimates with CIs without formal claims.
4. **Diagnostics**: seed-level difference distributions displayed (paired dot plots); normality not assumed (exact permutation test as primary inferential support; t-CI as interval estimate).
5. **Sensitivity analyses**: ECE recomputed with 10 bins; OOD AUROC recomputed with predictive entropy score. Conclusions are called robust only if direction and magnitude are stable.
6. All analysis code, raw metric JSON files, environment versions, and seeds are retained and released with the manuscript.

## 6. Stopping and exclusion rules

No data-dependent stopping. No test-set evaluation before all runs are complete. No exclusions of seeds or samples. Any failed run (NaN loss) would be re-run after a documented fix applied to all conditions and all seeds.

## 7. Predictions (falsifiable, fixed before test evaluation)

- H1: DeepEns-3 improves NLL over Single despite 3× shorter member training (diversity compensates for under-training).
- H2: Snapshot-3 underperforms DeepEns-3 on NLL (correlated snapshots reduce diversity).
- H3: SWA-3 improves accuracy over Single (weight averaging finds flatter minima) with NLL gains of unclear direction.
- H4 (exploratory, no inferential claim): DeepEns member disagreement exceeds Snapshot snapshot disagreement.

## 8. Reporting commitments

Effect sizes with 95% CIs and exact permutation p-values (Holm-adjusted for the primary family); figures show all five seed-level observations per condition, not only aggregates; any claim of "improvement" is tied to the paired CI; the boundary of inference (this architecture scale, this dataset family, this budget) is stated in the manuscript.
