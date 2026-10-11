# Extension Experiment Plan & Execution Report (Deliverable C)

**Status: EXECUTED in full on 11 October 2026** (this documents what was planned, what ran,
and the completion evidence — nothing below the "Completion evidence" line is aspirational).

## 1. Rationale (from audit items A-07 … A-11)

The v1 manuscript's main reviewer risks were: one dataset family, one shift probe, one budget,
one ensemble size, and no post-hoc recalibration baseline. The v2 extension addresses all five
within a CPU-only compute envelope, holding the v1 training procedure bit-identically fixed.

## 2. Design (all pre-specified before running, mirroring the v1 analysis plan)

| ID | Axis varied | Setting | Replicates | Total epochs |
|----|------------|---------|-----------|--------------|
| E-A | (v1 core re-run with extended evaluation) | Fashion-MNIST, B=60, k=3, probes {MNIST, KMNIST} | 10 | 1,620 |
| E-B | dataset direction | MNIST in-distribution, B=60, k=3, probes {FMNIST, KMNIST} | 10 | 1,620 |
| E-C | budget (low) | Fashion-MNIST, B=30, k=3 | 10 | 810 |
| E-D | budget (high) | Fashion-MNIST, B=120, k=3 | 10 | 3,240 |
| E-E | ensemble size | Fashion-MNIST, B=60, k=5 (members = 12-epoch runs) | 10 | 1,692 |

Shared v1 conventions (unchanged): base seed 10000+100s, member seeds base+11…, shared first
member between DeepEns and Snapshot (bit-identity re-verified for seed 0 of every setting),
SGD/momentum/weight-decay/LR-ceiling identical, 54k/6k split with the same split seed,
test sets touched once per condition per replicate.

**New measurement layer (applies to every condition of every setting):**
1. KMNIST as a second OOD probe (both directions), standardized with in-distribution stats.
2. Temperature scaling: one temperature per condition per replicate fitted on the 6,000-image
   validation split by minimizing validation NLL of softmax(z/T), where z is the raw-logit
   vector for single-model conditions and log of the averaged probabilities for ensembles
   (exactly Guo-style TS for single models by softmax shift-invariance). Reported: fitted T,
   TS-NLL, TS-ECE, TS-Brier, TS-AUROC per probe.
3. Replication of all v1 metrics (NLL/acc/Brier/ECE-15/ECE-10/AUROC-MSP/AUROC-entropy,
   member NLL, member acc, disagreement JSD).

**Statistical plan:** identical machinery to v1 (mean paired delta, 95% t-CI, exact sign-flip
permutation over all 2^10 patterns, Holm over the five contrasts). Families: raw NLL per
setting (primary-style, mirrors v1); TS-NLL per setting (labelled extension). Extension
settings are labelled non-preregistered throughout the manuscript.

**Fairness checks (budget-matched):** every condition consumes exactly B epochs of gradient
updates on the same 54k images; DeepEns and Snapshot share member 1; Snapshot and SWA share
all k checkpoints; the single 60-epoch model is identical across the k=3 and k=5 settings
(verified: identical per-seed NLL). Inference cost differences (k forward passes vs 1) are
discussed in the manuscript.

## 3. Execution timeline

- Environment rebuilt: torch 2.14.0+cpu (exact v1 version), torchvision 0.29.1, NumPy 2.1.3.
- datasets_v2.npz = v1 arrays (bit-identical, verified) + KMNIST test (downloaded from the
  official ROIS-CH mirror over HTTPS).
- **Reproduction gate (passed before any extension ran):** v2 pipeline re-ran seed 0 of E-A
  and matched all 28 recorded v1 metrics exactly (bit-level); shared-member bit-identity
  check passed.
- Queues executed in 11 foreground shards (the environment reaps background processes), with
  crash-safe per-replicate JSONL appends and done-seed skipping. Total wall-clock: 69 min
  (50 seed-runs, ~9,000 epochs). Every shard log line recorded per-replicate timings.
- Analysis: `analyze_v2.py` → `results/v2/analysis_v2.json` (+ CSVs). Figures:
  `make_figures_v2.py` → fig2/fig3/fig4 (+ per-panel source-data CSVs), VLM-checked.

## 4. Completion evidence

- Result files: `results/v2/experiment_v2_{fmnist_B60_k3, mnist_B60_k3, fmnist_B30_k3,
  fmnist_B120_k3, fmnist_B60_k5}.jsonl` — 10 records each, seeds 0–9, no gaps.
- `shared_member_bit_identical = true` recorded for seed 0 of every setting.
- All 50 records carry `wallclock_s`; totals reconcile with the shard logs (4,136 s).
- Headline outcomes (all Holm-adjusted within setting):
  - Ordering DeepEns > Snapshot > SWA > Single on NLL in all 5 settings (all contrasts
    p=0.0098), except Snapshot≈Single and SWA≈Single in the MNIST direction (p=0.41).
  - Budget-split advantage grows with budget (−0.075 → −0.225 → −0.332).
  - TS leaves DeepEns significantly best in every setting (TS-NLL vs Single: −0.0434,
    −0.0114, −0.0567, −0.0384, −0.0071; all p=0.0098).
  - OOD: DeepEns improves AUROC on all 4 probe–direction combinations; SWA never shows a
    reliable improvement beyond +0.011 on one probe (p=0.023 uncorrected).

## 5. What was deliberately NOT attempted (honest scope)

- CNN / CIFAR-10 / ImageNet-scale experiments: CPU-infeasible within this revision; stated
  in Limitations as future work rather than hidden.
- Other post-hoc calibrators (Platt, isotonic, beta calibration, Mix-n-Match compositions):
  only temperature scaling was run; the limitation is stated.
- Adversarial or corruption-based shift benchmarks; likelihood-based OOD scores.
- MIMO / hypernetwork ensembles (verification of bibliographic details incomplete).
