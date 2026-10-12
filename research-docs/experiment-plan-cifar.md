# Experiment plan: cross-architecture extension (CIFAR-10 + CNN)

**Status: planned before any test-set evaluation. This is a POST-HOC extension,
NOT part of the pre-registered v1 core analysis.** Written 2026-10-12, before
the first CIFAR training run. Documented following the same pre-specification
discipline as the v2 extensions.

## Motivation

The pre-registered core and all v2 extensions use one architecture family
(784-128-64-10 MLP) on grayscale 28x28 tasks. The single biggest external
validity threat is that the reported ordering may be an artifact of that
regime. This extension tests whether the core findings replicate under a
different architecture family (convolutional) and dataset (natural RGB images).

## Design

Mirrors the v1/v2 budget-matched design exactly, changing (model family,
dataset):

- **In-distribution task**: CIFAR-10 (50,000 train images, 32x32 RGB,
  10 classes). Train/val split: 45,000/5,000, fixed split seed 20261012
  (new documented split seed; permuting the 50,000-image training set).
- **OOD probe**: CIFAR-100 test set (10,000 images, 100 fine classes),
  standardized with the CIFAR-10 train-split statistics (same
  unknown-shift-at-deployment policy as v1/v2).
- **Preprocessing**: [0,1] scaling, per-channel standardization with train
  split mean/std. No data augmentation (mirrors the MLP protocol, where no
  augmentation was used; keeps budget accounting exact).
- **Model**: SmallCNN = Conv(3-16,3x3)-ReLU-MaxPool / Conv(16-32)-ReLU-MaxPool
  / Conv(32-64)-ReLU-MaxPool / FC(1024-10). ~34k parameters, no batch norm,
  no dropout (BN is deliberately avoided: BN running statistics interact with
  weight averaging and would confound the SWA contrast; the MLP study also
  used no normalization layers).
- **Optimizer**: SGD, momentum 0.9, weight decay 1e-4, batch 256, per-step
  cosine anneal from lr 0.1 to 0 (identical hyperparameter protocol to v1/v2).
- **Budget**: B=60 epochs, k=3 (the core setting). Conditions:
  Single (1x60), DeepEns (3x20), Snapshot (3-cycle cyclic run, 3 snapshots),
  SWA (uniform average of the same 3 snapshots).
- **Seeds**: 10 replicates, base = 10000+100*s, same member-seed convention
  (member i>=1 uses base+10+i). Seed 0 additionally verifies the
  shared-first-member bit-identity with a fresh 20-epoch run.
- **Compute accounting**: identical to v1/v2 — 2B + (k-1)B/k = 160 training
  epochs per replicate; identical optimizer-update counts across conditions.

## Hypotheses (falsifiable; all may fail)

- H1 (primary, NLL): DeepEns < Snapshot < SWA < Single on test NLL, with the
  five pre-specified contrasts directionally as in the MLP study.
- H2 (OOD): prediction averaging improves CIFAR-100 AUROC over Single
  (DeepEns and Snapshot), while SWA does not.
- H3 (recalibration): per-condition temperature scaling improves every
  condition's NLL but does not close the DeepEns-Single gap.
- H4 (mechanism): DeepEns members are better calibrated individually than
  Snapshot members; DeepEns members are more diverse (higher pairwise JSD).

Failure of any hypothesis is reported as such. If the ordering does not
replicate, the paper's claims will be narrowed accordingly (this would be an
informative boundary condition, not a reason to abandon the experiment).

## Statistical analysis

Same machinery as v2, labelled post-hoc: per-contrast exact sign-flip
permutation tests over 2^10 sign patterns, 95% t-intervals, Holm correction
across the five contrasts on raw NLL (one family) and on TS-NLL (second
family). Secondary metrics (acc, Brier, ECE, AUROC) reported with uncorrected
exact P values, labelled descriptive. The experimental unit is the seed.

## Cost estimate and fallback

Timing pilot on 2-3 epochs precedes the run. Measured: 12.5 s/epoch
(contiguous) / **8.0 s/epoch (channels_last memory format)** on 2 CPU cores;
channels_last is adopted for training and evaluation alike (a memory-layout
choice that does not alter the training computation's mathematics; within-run
determinism verified). Full run = 160 training epochs per replicate x 10
replicates + evaluation, ~3.7 h, executed in wall-clock shards with
epoch-level checkpointing; resume equivalence verified bitwise (interrupted
run == one-shot run, same schedule). Shared-first-member bit-identity and
pipeline correctness verified on a B=3 smoke run before the real run.

If pilot time had exceeded feasibility limits, the pre-specified fallback was
to reduce the budget to B=30 (keeping n=10 seeds and all contrasts), NOT to
reduce seeds below 10. With channels_last, B=60 (the core-mirroring setting)
is feasible and is used.

## Data provenance

CIFAR-10/CIFAR-100 obtained from the HuggingFace parquet mirrors of the
official Toronto releases (lossless PNG; verified: per-channel means
0.4914/0.4822/0.4465 and class counts match published statistics).
