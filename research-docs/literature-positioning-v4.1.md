# Literature Positioning and Novelty Audit v4.1

**Date:** 14 October 2026 · **Search channels used this session:** web search
(14 queries), arXiv API (keyword queries), OpenReview API (title/author/venue
verification), publisher pages (Springer DOI resolution, PMLR, CVF open
access). **Honesty rule:** "not found" is reported as "not found in the
channels searched", never as "does not exist".

---

## 1. Comparison matrix — closest related work (all entries verified against primary sources)

| Work | Question | Budget axis | Methods | Calibration | OOD | Checkpoint-matched pred-vs-weight | Seed-paired inference | Relation to this paper |
|---|---|---|---|---|---|---|---|---|
| Lakshminarayanan et al. 2017 (NeurIPS) | Do ensembles give good UQ? | none (added cost) | DeepEns vs MC-dropout etc. | yes | touched | no | no | Component method; the "expensive baseline" this study re-prices under a fixed budget |
| **Ashukha et al. 2020 (ICLR)** | In-domain UQ pitfalls; **compute-matched single vs ensemble (DEE score)** | partially (compute-matched figures) | Single vs DE (+ cheaper variants) | yes (NLL/coverage) | no | no | no | **Closest on contrast (i)**: covers ensemble-vs-single under matched compute, in domain. Differences: no snapshot/SWA, no epoch-allocation within a fixed architecture, no OOD, no TS interaction, no boundary conditions |
| **Brigato & Iocchi 2021 (arXiv:2111.14493)** | Ensemble effectiveness on small datasets | **fixed total compute** | Ensembles of small nets vs deeper/wider singles | accuracy focus | no | no | no | **Also covers (i)**, with architecture scaling as the alternative: ensembles competitive at fixed compute. Differences: architecture axis (not training-time allocation), accuracy endpoint, no calibration/OOD/TS |
| Fort et al. 2019 (arXiv) | Why restarts help (loss landscape) | none | DeepEns | partial | no | no | no | Mechanism background for the diversity measurements |
| Huang et al. 2017 (ICLR) | Free ensembles from cyclic LR | none (one run) | Snapshot | no | no | no | no | Component method |
| Izmailov et al. 2018 (UAI) | Weight averaging → flat minima | none | SWA | no | no | no | no | Component method |
| **Ramé et al. 2022 (NeurIPS, DiWA)** | Weight averaging for OOD **generalisation** | none (full runs combined) | WA across independent runs (DomainBed) | no | generalisation accuracy (not detection) | no | no | Adjacent on "weight averaging + shift": different endpoint (shifted-domain accuracy, not confidence-based detection/calibration), different unit (full runs, not budget-matched checkpoints). Cited in v4.1 to preempt conflation |
| Ovadia et al. 2019 (NeurIPS) | UQ under shift benchmark | varies across methods | many | yes | yes | no | no | Benchmark background; budgets not matched across methods |
| Guo et al. 2017 (ICML) | Calibration + TS | n/a | TS | yes | no | n/a | no | TS method adopted |
| **Krumpl et al. 2024 (WACV, ATS)** | Use adaptive TS to **improve OOD detection** | n/a | sample-specific TS + logits | no | yes (detection) | no | no | Directly supports the paper's TS-OOD claim: temperature rescaling is not rank-preserving on confidence scores. Cited in v4.1 |
| Zhang et al. 2020 (AISTATS) | Calibration + ensembles interaction | none | DE + calibrators | yes | no | no | no | TS-interaction precedent; no budget matching |
| Chirkova et al. 2020 (arXiv) | Fixed **memory** budget: 1 wide vs many thin | memory (params) | width-split ensembles | no | no | no | no | Fixed-resource analogue on the memory axis |
| Ajroldi et al. 2025 (ICML, PMLR v267) | When/where/why to average weights (AlgoPerf) | training **time** (acceleration) | WA variants | no (accuracy) | no | no | no | WA benchmark; acceleration/generalisation endpoints, no uncertainty quality, no pred-vs-weight checkpoint contrast |
| Thuy & Benoit 2024 (Ann. Oper. Res.) | Applied cheaper ensembles (industrial) | none stated | Single, DE, 3 efficient variants | yes (industrial) | no | no | no | Applied relevance; no matched budgets |
| **This paper** | How to spend a fixed **training budget** for calibrated uncertainty | **training epochs, exactly matched, one architecture** | Single, DeepEns, Snapshot, SWA (+ dense-SWA) | **yes (+ per-condition TS)** | **yes (11 setting×probe combos)** | **yes (identical checkpoints)** | **yes (exact permutation + Holm, n=10)** | — |

Additional works checked this session and judged non-overlapping (not
cited): Kumar et al. 2022 (AISTATS; calibrated ensembles of standard+robust
models for ID/OOD accuracy tradeoffs — different question);
Fredsgaard & Schmidt 2025 (arXiv 2511.04160; joint tuning of WD/TS/early
stopping in deep ensembles — no budget allocation);
Kurniawan et al. 2025 (arXiv 2508.06456; ensemble UQ for interatomic
potentials incl. snapshot ensembles — applied domain, budgets not matched);
ASWA 2024 (arXiv 2406.19092; adaptive SWA — not a comparison study);
model soups (WACV/ICML 2022; fine-tuning weight averaging — different
setting); Kalinke/Iocchi-line small-data ensemble studies (covered by
Brigato & Iocchi entry above).

## 2. What the re-check found (searches through 14 October 2026)

1. **Contrast (i) — fixed budget across restarts vs one long run — is NOT
   novel by itself.** Ashukha et al. (in-domain, compute-matched via DEE)
   and Brigato & Iocchi (fixed compute, architecture scaling) cover parts
   of it. The v4.0.0 positioning sentence claiming the re-check "did not
   surface a study covering any of these three contrasts" was therefore
   **inaccurate and internally inconsistent** with the paper's own Related
   Work; fixed in v4.1. What remains distinctive about (i) here: the
   budget is allocated across **training time of one fixed architecture**
   (epoch allocation, not width/depth), and the comparison includes the
   single-trajectory strategies a practitioner actually chooses between.
2. **Contrast (ii) — identical checkpoints combined by prediction vs weight
   averaging, evaluated for calibration and OOD detection — not found** in
   any channel searched. This is the paper's sharpest methodological
   contribution. Weight averaging has been studied extensively
   (Izmailov; Ramé/DiWA; Ajroldi) but always with accuracy/optimisation or
   shifted-domain-accuracy endpoints, and never checkpoint-matched against
   prediction averaging.
3. **Contrast (iii) — the joint interaction with per-condition TS and OOD
   detection — not found.** The nearest neighbour is ATS (Krumpl et al.
   2024), which *uses* temperature rescaling to improve OOD detection and
   thereby confirms the non-rank-preserving property this paper quantifies
   for uniform per-condition TS.
4. **Boundary conditions (near-saturated task; budget sweep direction;
   restart-failure documentation) are not covered** by any study found.

## 3. Novelty verdict after the re-check

- **Retained (defensible):** the compute-exact, checkpoint-matched,
  seed-paired four-way comparison design; the checkpoint-matched
  prediction-vs-weight contrast for calibration and OOD detection; the
  calibration-headroom boundary condition; the per-condition-TS stress test
  at matched budget; the member-quality/diversity measurements tied to the
  shared-first-member design.
- **Correctly narrowed in v4.1:** no claim of novelty for ensemble-vs-single
  budget comparisons as such (Ashukha; Brigato & Iocchi acknowledged);
  no claim about weight averaging under shift in general (DiWA
  acknowledged, different endpoint); no methodological novelty claimed
  anywhere ("ascriptive rather than algorithmic" retained).
- **Removed in v4.1:** the "did not surface a study covering any of these
  three contrasts" sentence (contradicted by Ashukha's own coverage of (i)).

## 4. Residual overlap risks (honest list)

1. **Un-indexed or very recent work.** The channels searched do not
   exhaust the literature; a concurrent study combining budget matching
   with the checkpoint-matched contrast may exist unseen. Mitigation: the
   positioning paragraph now dates the re-check (14 October 2026) and
   claims only what was checked.
2. **Domain-specific comparisons.** Applied fields (remote sensing,
   medical imaging, materials science — e.g. the Kurniawan et al. 2025
   interatomic-potentials study) sometimes run ensemble-variant
   comparisons that resemble parts of the design. None found matches the
   checkpoint-matched contrast with calibration/OOD endpoints, but domain
   literatures are only partially indexed by the channels available.
3. **Brigato & Iocchi is an arXiv preprint.** If a peer-reviewed version
   exists (none found via arXiv journal-ref or search), the citation
   should be updated at proof stage.
