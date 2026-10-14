# Claim–Evidence Matrix v4.1

**Manuscript:** v4.1.0 (14 October 2026) · **Evidence base:** raw per-seed
JSONL records (6 settings × 10 seeds + SWA-dense), independently
recomputed this session; literature re-check through 14 October 2026.
**Legend:** SUPPORTED = keep · LIMITED = only a bounded/conditional claim is
supported · FIXED = changed in v4.1 (was inaccurate in v4.0.0) ·
AUTHOR = needs author confirmation.

---

## A. Abstract

| Claim (v4.1 wording) | Evidence | Verdict |
|---|---|---|
| Every strategy improved test NLL over Single at the core budget (Holm P=0.0098), ordered DeepEns > Snapshot > SWA > Single on NLL and calibration error | All five contrasts recompute exactly; all ten seeds agree in direction; ECE ordering strict in the core setting (0.0236 < 0.0444 < 0.0517 < 0.0702) | SUPPORTED |
| The ordering held across budgets (30–120), ensemble sizes (k=3, 5) | Four-way ordering strict on NLL **and** every in-distribution metric at B=120; on NLL at all Fashion-MNIST settings; all five contrasts Holm-significant per setting | SUPPORTED |
| …and, post-hoc, CIFAR-10, where the DeepEns–Snapshot calibration-error advantage was directionally consistent but not statistically resolved | Mean ECE ordering holds (0.0407 < 0.0826 < 0.1454 < 0.2213) but DE−SN ECE = −0.0418, CI [−0.0845, +0.0008], P=0.082; NLL contrasts all significant | LIMITED (stated as such) — FIXED vs v4.0.0 which implied robustness without the ECE boundary |
| Bounded exceptions at the lowest budget | B=30 accuracy (Snapshot 0.8929 > DeepEns 0.8905) and Brier (0.1562 vs 0.1573) reversals ≤ 0.003, never touching NLL/ECE; TS equalisation at B=30 | SUPPORTED |
| On the near-saturated MNIST task only DeepEns separated from Single; single-trajectory strategies showed no reliable improvement | DE−SG −0.0158 adj P=0.0098; SN−SG −0.0015 P=0.41; SWA−SG +0.0017 P=0.41 | SUPPORTED — FIXED vs v4.0.0 ("ordering was robust across … a reversed dataset direction" — the four-way mean ordering does not hold there: SWA 0.0741 > Single 0.0724 NLL, 0.0101 > 0.0098 ECE) |
| OOD: prediction averaging improved over Single on every probe and direction; weight averaging smaller, task-dependent (−0.016 to +0.025), significant on some settings, reversed on one | DeepEns positive on all 11 setting×probe combos (family-adjusted P ≤ 0.032); SWA 5 positive-sig / 1 negative-sig / 5 null; entropy-score range −0.0147…+0.0306 | SUPPORTED |
| TS repaired much of every condition's miscalibration, left DeepEns significantly best at core budget and above (0.289 vs 0.333), largely equalised ensembles at B=30 | TS-NLL contrasts: core DE−SG −0.0434 adj 0.0098; B120/k5/MNIST DE−SG all adj 0.0098; B=30 span 0.2986–0.3126 with Snapshot nominally best and DE−SN reversed (+0.0026, adj P=0.045) | SUPPORTED (B=30 equalisation stated) |
| Evidence bounded to small networks and image tasks; rule conditional on calibration headroom | Two architectures ≤ 110k params, epoch-denominated budgets; MNIST boundary condition measured | SUPPORTED (scope statement) |

## B. Introduction (contributions)

| Claim | Evidence | Verdict |
|---|---|---|
| Compute-exact four-way design; shared first member bit-identical; Snapshot/SWA identical checkpoints | Design fact; verified programmatically in both pipelines (records carry `shared_member_bit_identical: true` for all 60 replicates) | SUPPORTED |
| Lowest mean test NLL in every setting; four-way ordering held on NLL across budgets/sizes/CIFAR; MNIST boundary as stated | See A; MNIST DE best is directly supported (DE−SN, DE−SG, DE−SWA all significant; DE−SWA now a direct test) | SUPPORTED — FIXED vs v4.0.0 ("stable across … both dataset directions") |
| ECE mean ordering held in every setting with all DE−SG contrasts significant; DE−SN ECE unresolved on CIFAR | DE−SG ECE: −0.0466/−0.0343/−0.0466/−0.0561/−0.0051/−0.1805, all P=0.0020; DE−SN CIFAR P=0.082 | LIMITED (stated as such) — FIXED |
| Boundary condition (MNIST) | See A | SUPPORTED |
| OOD separation of combination mechanisms | See A | SUPPORTED |
| TS stress test (compresses but does not close gaps at core budget and above; ≤ +0.012 digit shifts, up to +0.026 CIFAR; B=30 equalisation) | Recomputed per-condition TS deltas | SUPPORTED |
| Cross-architecture replication incl. member-level mechanism measurements | CIFAR member NLL 1.0676 vs 1.2288; JSD 0.1545 vs 0.0915; ordering + OOD separation replicated | SUPPORTED (measurements descriptive; §4.5 keeps the associational caveat) |

## C. Main results (§4.1–4.2)

All numbers in Tables 1–3 and the surrounding text recompute exactly from
`results/experiment.jsonl` and `results/v2/*.jsonl` (200+ checks; one
display error fixed: Table 1 KMNIST s.d. row). **Verdict: SUPPORTED**, with
the two evidence-boundary statements (CIFAR ECE; MNIST non-separation of
single-trajectory strategies) carried through from the abstract.

## D. Temperature scaling (§4.3)

| Claim | Evidence | Verdict |
|---|---|---|
| TS helps every condition; Single NLL 0.5265→0.3325, ECE 0.0702→0.0111; fitted T ordering 2.46/1.79/1.58/1.25 | Recomputed | SUPPORTED |
| Ordering persists after per-condition TS at core/budget and above; B=30 equalisation | Table S3 recomputed exactly | SUPPORTED |
| Digit-task OOD shifts ≤ +0.012; CIFAR +0.004…+0.026; gap compression +0.069→+0.046, no reversal | Recomputed per condition | SUPPORTED |
| TS is not rank-preserving on confidence scores in general; effect is empirical | Theoretical statement is correct (softmax(z/T) max depends on the whole logit vector; ensemble z = log p̄ mixes members); ATS (WACV 2024) uses this freedom deliberately | SUPPORTED (literature-anchored; citation added in v4.1) |

## E. OOD (§4.4)

| Claim | Evidence | Verdict |
|---|---|---|
| Core-setting contrasts, CIs and P values (incl. SWA nulls with cautious-reading note) | Table S4 recomputed exactly | SUPPORTED |
| Snapshot/SWA difference reflects only the combination rule; mechanism reading marked as a reading | Design fact + interpretive framing | LIMITED to the interpretive parts — FIXED ("attributable…alone: transfers…" → "reflects…; a reading consistent with…") |
| DeepEns best mean detection on every combination, only strategy significant on all 11 within per-probe families (P ≤ 0.032) | Recomputed counts 11/11, 9/11, 5/1/5 | SUPPORTED (rounding fixed) |
| Global 55-contrast family: nothing survives, DeepEns included; conclusions rest on effect size and cross-setting consistency | Floor 0.0020 × 55 = 0.11 > 0.05; recomputed | SUPPORTED |
| SWA-SWA-dense leaves OOD unchanged from Single | Table S2 recomputed | SUPPORTED |

## F. Mechanism (§4.5) and cross-architecture (§4.6)

| Claim | Evidence | Verdict |
|---|---|---|
| Member calibration/diversity measurements (core, k=5, CIFAR) | All recomputed exactly | SUPPORTED |
| Associational wording ("associate the mechanism with the outcome rather than establishing it causally") | Kept and strengthened ("two measurable ingredients") | SUPPORTED (bounded) |
| CIFAR replication statements incl. ECE contrast with CI/P and the anomalous-replicate account | Recomputed exactly, incl. diagnosis file and leave-one-out sensitivities | SUPPORTED |
| "unique among the twenty fresh restarts" | Member-level accuracy of all 10 replicates consistent with exactly one collapsed restart | SUPPORTED |

## G. Discussion, Conclusion, Declarations

| Claim | Evidence | Verdict |
|---|---|---|
| Opening allocation-rule summary | Scoped to primary outcome; causal wording tightened — FIXED ("attributable to … rather than trajectory noise" → split into allocation/rule statement + checkpoint-sharing statement) | SUPPORTED after fix |
| Practitioner guidance (conditional TS advice; inference-cost paragraph) | Bounded by measured evidence; inference cost distinction kept | SUPPORTED |
| Limitations (architecture scale, single natural-image task, epoch-denominated budget, inference cost, OOD families post-hoc, mechanism associational, restart-failure rates unknown) | Accurate | SUPPORTED |
| AI-use disclosure | Extended to cover this revision; matches Springer policy (LLM use documented; LLM not an author) | SUPPORTED — AUTHOR to confirm accuracy of the description |
| Conflict of interest, funding, author contribution | Not stated beyond COI ("none") — **IJMLC requires Author Contribution and Competing Interest via the submission interface** | AUTHOR |
| ORCID, submission-interface fields, cover letter | Author actions at submission time | AUTHOR |

## H. References

All 28 entries verified this session or in the documented v2/v3 verification
chain (the four newest: Ajroldi ICML 2025 via PMLR v267 + OpenReview; Thuy &
Benoit via resolving DOI 10.1007/s10479-024-06440-4; Krumpl WACV 2024 via
CVF open access; Ramé NeurIPS 2022 via arXiv/proceedings). **Verdict:
SUPPORTED.** Residual risk: Brigato & Iocchi (2021) is an arXiv preprint; the
journal prefers published work but accepts preprints; flagged in the
submission checklist.
