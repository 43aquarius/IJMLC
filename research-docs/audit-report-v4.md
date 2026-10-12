# Research Audit Report v4 (Deliverable A)

**Manuscript:** "Deep ensembles outperform snapshot ensembles and weight
averaging for calibrated uncertainty under fixed training budgets" — v4
(24 pp., 13 October 2026; v3 was 21 pp., 12 October 2026)
**Target journal:** International Journal of Machine Learning and Cybernetics
**Audit date:** 13 October 2026 (session 4)
**Auditor roles:** ML researcher / IJMLC reviewer / statistics auditor /
experimental-reproduction engineer / English editor

---

## 1. Version and evidence-chain verification (Phase 1 of the directive)

1. **File identity.** The uploaded `main_v3.pdf`, the repository's
   `paper/main_v3.pdf`, `paper/budget-matched-ensembles-paper.pdf` and the
   `paper-v3.0.0` Release asset are byte-identical (SHA-256
   `141912b6f2a7b1921fbac59eedbf516fc4b655ced86222b105ca1122a52f4947`,
   verified across all copies). A fresh `tectonic` compile of
   `manuscript-source/main.tex` reproduces the published v3 PDF with all 21
   pages text-identical (the only difference is the embedded creation
   timestamp). The v3 under audit is therefore exactly the repository
   version; no divergent uploaded copy exists.
2. **Raw data re-read.** All six settings' per-seed JSONL (5 MLP settings +
   CIFAR), the analysis JSONs/CSVs, and the v3 research documents were read
   and re-verified. All contrast statistics in `analysis_v2.json` and
   `analysis_cifar.json` reproduce exactly under independent recomputation
   from the raw records (`code/reanalysis_v4.py`; exact sign-flip
   enumeration, t-intervals, Holm).
3. **Prior audit reports were treated as claims, not evidence.** Two v3
   claims failed re-verification against the raw data (V4-01, V4-02 below)
   despite v3 documents marking them resolved — precisely the failure mode
   the directive warned about.

## 2. v4 issue register

Priorities: **P0** = statement contradicts the data · **P1** = likely
reviewer objection · **P2** = weakens paper · **P3** = polish.

| ID | Pri | v3 statement (location) | Problem found (evidence) | v4 resolution | New experiment? | Verification |
|----|-----|--------------------------|--------------------------|---------------|-----------------|--------------|
| V4-01 | **P0** | "Only prediction averaging improved OOD detection ... SWA showed no improvement surviving multiple-comparison correction" (Abstract; contributions bullet; §4.4; Discussion; Conclusion) | Contradicted by the paper's own data under the same family structure used for the NLL analyses: within each setting-probe 5-contrast Holm family, SWA-Single is significantly positive on 5/11 combinations (core KMNIST +0.0112, adjusted P=0.023; both B=30 probes; k=5 KMNIST; CIFAR-100 +0.0247, adjusted P=0.0098), significantly negative on 1/11 (B=120 MNIST probe -0.0157, adjusted P=0.012), null on 5/11 | Rewritten in all five locations to the comparative form: prediction averaging larger and consistent (DeepEns significant 11/11; Snapshot 9/11); weight averaging smaller (-0.016..+0.025) and task-dependent. §4.4 now defines the OOD multiplicity families explicitly, marks them post-hoc, reports all three family sizes for every strategy, and states the global-family caveat (nothing survives 55 tests, DeepEns included) | No (re-analysis of existing data) | 34/34 automated number checks (`code/verify_v4_numbers.py`); Table S4 generated programmatically |
| V4-02 | **P0** | "TS changed OOD AUROC by at most +0.012 on any condition or probe" (§4.3); "it changes confidence levels, not their ranking across inputs" (Discussion) | (i) Scope error: CIFAR-100 shifts reach +0.0260 (Single), +0.0186 (SWA), +0.0165 (Snapshot). (ii) Theory error: softmax(z/T) is not a rank-preserving transform of the maximum softmax across samples (the scaled max depends on the whole effective-logit vector; for ensembles z = log mean-prob mixes members), so cross-sample rankings can change | §4.3 scoped to the digit tasks with the CIFAR shifts and the gap compression (+0.069 -> +0.046) reported; Discussion sentence rewritten to the not-rank-preserving-in-general form with the empirical heterogeneity; practitioner guidance made conditional | No | verified against per-condition TS deltas (reanalysis §6) |
| V4-03 | **P1** | §4.6: "the pattern extended to every in-distribution metric, including accuracy ... and ECE" | Mean-ordering true, statistical evidence missing for the CIFAR DeepEns-Snapshot ECE contrast: -0.0418, 95% CI [-0.0845, +0.0008], raw P=0.082 | §4.6 now reports the contrast with CI and P, distinguishing mean ordering from statistical resolution; abstract/contributions scoped accordingly; the unresolved-ness is attributed to (and only to) the collapsed replicate, with the drop-8 sensitivity also reported | No | reanalysis §7, §8 |
| V4-04 | **P1** | §4.6: "One of the ten replicates reversed the DeepEns-Snapshot ordering at seed level" (cause unexplained) | Diagnosis performed: the replicate's second fresh restart (seed 10812) collapsed to uniform predictions in epoch 1 (train loss ~ln 10 from epoch 1; logits -> 0; accuracy ~0.10) and never recovered — a dead-network collapse under lr 0.1 without normalisation layers; verified by deterministic re-run with the shared member reproducing bit-identically | New §4.6 paragraph: diagnosis, retention under the no-exclusion rule, LOO sensitivity (drop-8 strengthens DE-SN: NLL -0.2075, ECE -0.0607, P=0.0039), and the practitioner-facing reading (restart risk; the ensemble still beat Single 0.929 vs 2.017) | No (diagnostic reproduction, same seeds) | `results/v4/seed8_diagnosis.json`; report C |
| V4-05 | **P1** | OOD results reported only for the core and MNIST-direction settings; B=30, B=120, k=5 OOD never shown | Selective reporting risk: the unreported settings contain SWA's significant positives (B=30) and significant negative (B=120) | New Supplementary Table S4 with all 11 setting-probe combinations x 3 vs-Single contrasts (delta, CI, raw P, Holm P); §4.4 summarises the full pattern | No | table generated from reanalysis JSON |
| V4-06 | **P2** | §3.5 labelled OOD "reported uncorrected throughout" but no corrected OOD analysis had been defined anywhere, while §4.4 simultaneously claimed (wrongly, V4-01) SWA's effects did not survive correction | Multiplicity framework incomplete for the claims being made | §3.5 now specifies: pre-specified primary reporting = uncorrected exact P; post-hoc robustness = Oa (per setting-probe-score Holm), Ob (setting-level), Oc (global 55); labelled post-hoc with the definition date disclosed (after CIFAR results known); Limitations repeats the labelling | No | reanalysis families F1/F2/Oa/Ob/Oc |
| V4-07 | **P2** | `download_data_cifar.py` printed per-channel means [0.329, 0.329, 0.329] — its own integrity check appears to fail | Float32 accumulation bug in the check line only (5.1e7 sequential additions); the stored data are correct (float64 recomputation gives 0.4914/0.4822/0.4465, matching official statistics; pixels verified against the parquet source) | Fixed to float64 with an explanatory comment; code-audit report updated | No | verified in this session |
| V4-08 | **P2** | Fig. 4b caption "SWA tracks Single throughout" | Fine for the four digit combos shown, but could read as a global claim after the §4.4 changes | Caption softened to "stays closest to Single" | No | visual QA |
| V4-09 | **P3** | Practitioner guidance "apply temperature scaling regardless ... does no harm to shift detection" | "No harm" as an unconditional claim exceeds the evidence | Conditionalised: nearly free, repaired overconfidence everywhere here, but its effect on confidence-based shift scores should be checked in the target setting | No | manual |
| V4-10 | **P3** | Title "outperform ... for calibrated uncertainty" | Anchored on the primary outcome (NLL) with bounded secondary-metric exceptions; kept after re-review | Unchanged; the abstract and contributions now make the primary-outcome anchoring explicit; rejected alternatives documented (v3 revision log) | No | manual |

**Resolved in v3 and re-confirmed this session (not re-opened):** budget
matching (identical optimizer-update counts), OOD orientation (MSP with ID
as positive class; negative-entropy score orientation correct in code and
consistent across settings), temperature-scaling implementation (log-prob
effective logits; exact single-model equivalence; per-condition fitting on
validation only), shared-member bit-identity (seed 0, both pipelines),
channels_last claim (used in both training and evaluation in the actual
runner), citation numbering, author block, declarations, IJMLC formatting,
timing statements, repository structure.

## 3. Statistical audit summary

1. **Independent recomputation:** every contrast estimate, CI, permutation P
   and Holm P in the released analysis files reproduces exactly from the raw
   per-seed records (all six settings; sign-flip enumeration over 2^10
   patterns).
2. **P-value resolution:** with n=10, the two-sided sign-flip floor is
   0.0019531 (uncorrected) and 0.0098 (5-contrast Holm). Repeated P=0.0098
   values are direction-unanimity statements at the test's resolution, not
   effect-magnitude evidence; §3.5 states this and the results note it at
   first use.
3. **Analysis-tier separation:** pre-registered core (F1), pre-specified TS
   family (F2), post-hoc extensions (B/k/direction/probes/CIFAR), post-hoc OOD
   families (Oa/Ob/Oc, definition date disclosed), exploratory dense-SWA.
   No post-hoc analysis is described as pre-registered anywhere in v4.
4. **No family cherry-picking:** all three OOD family sizes are reported for
   every strategy; the qualitative conclusion (prediction averaging larger
   and more consistent) is stable across families, while the categorical
   "SWA never improves" claim — not stable across families — was removed.
5. **No outcome-based exclusions:** all ten seeds retained everywhere; the
   collapsed replicate is reported, diagnosed, and carried through the
   primary analysis with an explicitly labelled sensitivity view.

## 4. Remaining items and their status

| Item | Status |
|---|---|
| Corruptions/perturbations OOD benchmark (e.g., CIFAR-10-C) | Not run; stated as future work (Limitations); template + code released to make it mechanical |
| Larger networks / normalisation layers / transformers | Not run; claims explicitly bounded to the tested regime |
| Cross-hardware bit-exact reproduction | Not possible on one machine; tolerance-level reproduction verified in kind (shared member matches to 6 decimals across two wheel builds; collapsed-member endpoint differs at the dead-state level — documented in report C) |
| ORCID / journal-template port / submission-interface fields | Author actions at submission time (checklist) |
| Cover letter | Updated to v4 form (checklist §6) |
