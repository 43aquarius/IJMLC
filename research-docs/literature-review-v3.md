# Literature Review and Novelty Assessment v3 (Deliverable B)

**Date:** 12 October 2026 · **Manuscript:** budget-split ensembles paper (v2 → v3)
**Search window emphasised:** 2024–2026 (re-check), on top of the v2 verification of
the 21 core references (11 October 2026).

## 1. Verification status of the search process

- Searches executed via the web-search backend; results logged under
  `tool-results/litsearch_v3/` (12 initial queries + follow-ups). The arXiv API and
  Semantic Scholar API were rate-limited from this environment (HTTP 429), so
  bibliographic details for the two most adjacent papers were confirmed through the
  OpenReview API (full records, including author lists and venue) and publisher pages.
- No reference is included below without a verified title + author list + year +
  venue from at least one authoritative source. Where only partial metadata could be
  verified, the work is listed in §5 as *not cited* rather than risk a fabricated
  citation.

## 2. The comparison matrix — how the closest prior work differs

| Work | Question | Budget axis | Methods compared | Calibration | OOD | Checkpoint-matched contrast | Seed-paired inference |
|------|----------|------------|------------------|-------------|-----|-----------------------------|----------------------|
| Lakshminarayanan et al. 2017 (NeurIPS) | Do ensembles give good UQ? | none (added cost) | DE vs MC-dropout etc. | yes | touched | no | no |
| Ashukha et al. 2020 (ICLR) | In-domain UQ estimation pitfalls; compute-matched single vs ensemble | partially (compute-matched figs) | Single vs DE (+ diversification) | yes | no | no | no (error bars only) |
| Fort et al. 2019 (arXiv) | Why do restarts help? (loss landscape) | none | DE | partial | no | no | no |
| Huang et al. 2017 (ICLR) | Free ensembles from cyclic LR | none (one run) | Snapshot | no | no | no | no |
| Izmailov et al. 2018 (UAI) | Weight averaging → flat minima | none | SWA | no | no | no | no |
| Ovadia et al. 2019 (NeurIPS) | UQ under shift benchmark | varies across methods | many | yes | yes | no | no |
| Guo et al. 2017 (ICML) | Calibration + TS | n/a | TS | yes | no | n/a | no |
| Zhang et al. 2020 (AISTATS) | Mix-n-match calibration+ensembles | none | DE + calibrators | yes | no | no | no |
| Chirkova et al. 2020 (arXiv:2005.07292) | Fixed **memory** budget: 1 wide vs many thin | memory (params) | width-split ensembles | no | no | no | no |
| Whitaker et al. 2022 (AAAI) | Low-cost ensembles by pruning | low training budget | pruned ensembles | partial | no | no | no |
| Thuy & Benoit 2024 (arXiv / Ann. Oper. Res.) | Applied: cheaper ensembles for industrial inspection | none stated | Single, DE, 3 efficient-ensemble variants | yes (industrial) | no | no | no |
| **Ajroldi, Orvieto, Geiping 2025 (ICML)** | When/where/why to average weights (AlgoPerf benchmark) | training **time** (acceleration) | weight averaging variants | **no** | **no** | **no** | no |
| **This paper (v3)** | How to spend a fixed **training budget** for calibrated uncertainty | **training epochs, exactly matched** | Single, DeepEns, Snapshot, SWA (+ dense-SWA exploratory) | **yes (+ per-condition TS)** | **yes (4 probe-direction combos)** | **yes (Snapshot and SWA share identical checkpoints; DeepEns and Snapshot share member 1 bit-identically)** | **yes (exact permutation + Holm, n=10)** |

## 3. Novelty verdict after the 2024–2026 re-check

1. **Uncovered (retain):** the four-way budget-matched allocation comparison with
   seed-paired exact permutation inference; the checkpoint-matched
   prediction-averaging vs weight-averaging contrast evaluated for calibration
   and OOD detection; the interaction of that contrast with per-condition
   temperature scaling. No 2024–2026 work found that does any of these.
2. **Covered elsewhere (already correctly narrow in v2):** single-vs-deep-ensemble
   compute-matched comparisons (Ashukha et al. 2020); why restarts help (Fort et al.
   2019); ensembles robust under shift (Ovadia et al. 2019); calibration of
   ensembles vs recalibrated singles (Zhang et al. 2020).
3. **Adjacent but distinct (new citations needed, see §4):** weight-averaging
   benchmarking for training acceleration (Ajroldi et al. 2025) — complementary:
   they optimise for speed/generalisation, we measure uncertainty quality;
   fixed-memory ensemble splitting (Chirkova et al. 2020) — the memory-budget
   analogue; applied cheaper-ensemble studies (Thuy & Benoit 2024).

## 4. Reference-list changes for the v3 manuscript (all verified)

**Added:**
1. Ajroldi, N., Orvieto, A., Geiping, J.: When, where and why to average weights?
   In: International Conference on Machine Learning (ICML 2025, poster). [verified
   via OpenReview API: authors, title, venue]
2. Chirkova, N., Lobacheva, E., Vetrov, D.: Deep ensembles on a fixed memory
   budget: one wide network or several thinner ones? arXiv:2005.07292 (2020)
   [verified via Google Scholar record surfaced in search]
3. Thuy, A., Benoit, D.F.: Reliable uncertainty with cheaper neural network
   ensembles: a case study in industrial parts classification. arXiv preprint
   (2024); journal version: Fast and reliable uncertainty quantification with
   neural network ensembles for industrial image classification, Annals of
   Operations Research (2024), DOI 10.1007/s10479-024-06440-4 [verified via
   Crossref + search snippets]

**Positioning sentences added to Related Work:**
- Weight averaging as an *optimisation accelerator* (Ajroldi et al. 2025) is
  complementary to our finding that it does not buy shift robustness: their
  AlgoPerf evidence concerns generalisation and wall-clock, not uncertainty
  quality, and does not include the prediction-averaging contrast.
- The fixed-resource framing extends to memory (Chirkova et al. 2020); our
  study is the training-compute axis with calibration and OOD endpoints.
- Applied studies adopt cheaper ensembles for reliability (Thuy and Benoit 2024),
  which supports the practical relevance of allocation questions but does not
  answer them under matched budgets.

**Rejected candidates (could not verify sufficiently; NOT cited):**
- "Uncertainty Calibration in Deep Learning: Methods, …" (2026 survey, author
  "M.L. Zhang") — venue could not be verified from available sources (sciopen/ACM
  links without a resolvable journal record); omitting rather than risking an
  inaccurate entry.
- "Snapshot ensemble learning with attention-enhanced CNNs" (2026) — title-only
  visibility; not needed for our claims.

## 5. Final contribution statement (v3, evidence-bounded)

This paper's contribution is **not** a new method. It is (i) a compute-exact,
checkpoint-matched, seed-paired **comparison design**; (ii) a **robust NLL/ECE
ordering result** for budget-split restarts across five Fashion-MNIST settings, one
reversed dataset direction, and (new in v3) a CIFAR-10 CNN replication; (iii) a
**boundary condition** (near-saturated tasks); (iv) a **mechanism separation**
(prediction averaging vs weight averaging on identical checkpoints) extended to OOD
detection and post-hoc recalibration. All claims are bounded to the regimes tested:
small networks (≤ ~110k parameters), image classification, epoch-denominated
budgets, confidence-based OOD scores.
