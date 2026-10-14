# Number Verification Report v4.1 (independent recomputation)

**Date:** 14 October 2026 · **Method:** every number below was recomputed
directly from the raw per-seed JSONL records by an independent
implementation (exact sign-flip enumeration over 2^10 patterns,
t-intervals, Holm step-down with monotonicity enforcement), without
reading any value from the released analysis JSONs. Scripts:
`scripts/verify_v41_stage1.py`, `_stage2.py`, `_stage3.py` (persisted).

- Tables 1-3, TS section: **84/89 checks passed**
- Table S4, ECE contrasts, CIFAR, seed 8: **84/85 checks passed**
- DE-SWA direct, orderings, Tables S1/S2, budget sweep, wall-clock: **64/67 checks passed**

**Overall: 232/241 checks passed.**

## Failures and their dispositions

| Check | Claimed (v4.0.0) | Recomputed | Disposition |
|---|---|---|---|
| Tab1 single.auroc_msp_kmnist | 0.6951±0.0184 | 0.6951±0.0116 | Table 1 s.d. corrected to 0.0116 (v4.1 edit #1) |
| Tab1 deepens.auroc_msp_kmnist | 0.8048±0.0067 | 0.8048±0.0038 | Table 1 s.d. corrected to 0.0038 (v4.1 edit #1) |
| Tab1 snapshot.auroc_msp_kmnist | 0.7536±0.0131 | 0.7536±0.0084 | Table 1 s.d. corrected to 0.0084 (v4.1 edit #1) |
| Tab1 swa.auroc_msp_kmnist | 0.7063±0.0132 | 0.7063±0.0112 | Table 1 s.d. corrected to 0.0112 (v4.1 edit #1) |
| ordering ECE mnist | DE<SN<SWA<SG in means | computed above | Mean ordering DE<SN<SWA<SG fails on MNIST (SWA 0.0101 > SG 0.0098); abstract/contribution wording corrected (v4.1 edit #2) |
| S4.6/report C | other nine member acc 0.7257±0.0042 | 0.7249±0.0042 | Research-doc-only value ('other nine member acc 0.7257' vs recomputed 0.7249); manuscript not affected; research doc annotated |
| ordering ECE mnist | DE<SN<SWA<SG | see above | Mean ordering DE<SN<SWA<SG fails on MNIST (SWA 0.0101 > SG 0.0098); abstract/contribution wording corrected (v4.1 edit #2) |
| ordering NLL mnist | DE<SN<SWA<SG | DE 0.0565 SN 0.0709 SWA 0.0741 SG 0.0724 | Mean ordering fails on MNIST (SWA 0.0741 > SG 0.0724); abstract/contribution wording corrected (v4.1 edit #2) |
| S3.3 | CIFAR ~3.5 hours | 0.94 h | CIFAR wall-clock: JSONL records only the final shard per replicate (56 min total recorded); the ~3.5 h claim is consistent with the pre-run timing pilot (8.0 s/epoch x 1,600 epochs = 3.6 h, documented in experiment-plan-cifar.md); claim kept as an execution-time statement |

## Verified-but-not-re-executed items (documented provenance)

| Item | Provenance | Status |
|---|---|---|
| Clean-environment 110/110 bit-for-bit seed-0 gate | `research-docs/code-audit-report-v3.md` (session of 12 Oct 2026) | Documented; not re-executed this session |
| v2-pipeline-reproduces-v1 28/28 (seed 0) | `results/verification_seed0.json` + v2 session log; cross-checked this session at 200/200 comparisons over all 10 seeds for the shared metrics | Verified this session (all 10 seeds) |
| CIFAR sharded-execution resume equivalence; shared-member bit-identity (CIFAR) | experiment-plan-cifar.md + code-audit-report-v3.md | Documented; not re-executed |
| Seed-8 deterministic diagnosis | `results/v4/seed8_diagnosis.json` re-read this session; collapse pattern (member 2: epoch-1 train loss 2.2999 ~ ln 10, logits 0.0142 by epoch 20, acc 0.10, NLL 2.3026) and all manuscript numbers confirmed | Verified against the diagnosis file |

## Notes

1. The exact two-sided sign-flip floor with n=10 is 2/1024 = 0.0019531
   (reported as 0.0020); the Holm floor within a five-contrast family is
   0.0098. Every P=0.0020 entry in the manuscript corresponds to all ten
   seeds agreeing in direction - a resolution statement, not an effect-size
   statement. The manuscript states this at first use (S3.5).
2. All Holm adjustments were recomputed with step-down monotonicity; the
   v4.0.0 Table S4 Holm column reproduces exactly (one rounding fix in the
   running text: P <= 0.031 -> <= 0.032).
3. New analysis added in v4.1 (re-analysis of existing data, no new
   experiment): the direct DeepEns-SWA contrast on MNIST NLL:
   **-0.0176, 95% CI [-0.0199, -0.0153], uncorrected exact P=0.0020**
   (all ten seeds agree). This replaces the v4.0.0 'by adjacency'
   inference.
