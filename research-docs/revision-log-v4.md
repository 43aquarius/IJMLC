# Revision Log v3 → v4 (Deliverable E)

**Manuscript:** "Deep ensembles outperform snapshot ensembles and weight
averaging for calibrated uncertainty under fixed training budgets" (v4,
13 October 2026). "v4 location" refers to v4 section numbering.

## Modification table

| # | Original problem (v3) | Modified content (v4) | Basis | New experiment needed? | Verification status |
|---|------------------------|------------------------|-------|------------------------|---------------------|
| V4-01 | Abstract / contribution bullet / §4.4 / Discussion / Conclusion claimed "Only prediction averaging improved OOD detection" and "SWA showed no improvement surviving multiple-comparison correction" | All five locations replaced with the comparative, heterogeneity-reporting form: prediction averaging improves OOD on every probe-direction combination with the largest gains (DeepEns significant 11/11 within the per-probe Holm family); weight averaging's effects are smaller (-0.016..+0.025), significantly positive on 5/11 (core KMNIST +0.0112 adj. P=0.023; B=30 both probes; k=5 KMNIST; CIFAR-100 +0.0247 adj. P=0.0098), significantly negative on 1/11 (B=120 MNIST probe -0.0157 adj. P=0.012), null on 5/11 | Independent recomputation from raw JSONL (`code/reanalysis_v4.py`); within-probe 5-contrast Holm families mirroring the pre-specified NLL family structure; setting-level and global (55-test) sensitivities reported alongside | No (re-analysis) | 34/34 automated checks (`code/verify_v4_numbers.py`); Table S4 generated programmatically from the same data |
| V4-02 | §4.3: "TS changed OOD AUROC by at most +0.012 on any condition or probe" — false once CIFAR is included (Single +0.0260, SWA +0.0186, Snapshot +0.0165) | Scoped to the digit tasks; CIFAR-10 shifts and the DeepEns-Single gap compression (+0.069 → +0.046) reported; §4.3 also explains why TS is not rank-preserving across samples in general | Per-condition TS deltas from raw records (reanalysis §6); softmax(z/T) max-score ranking analysis | No | Number check V4-02 in verifier; manual theory review |
| V4-03 | Discussion: "Under shift, temperature scaling bought nothing—it changes confidence levels, not their ranking across inputs" — theoretically false (not a rank-preserving transform, esp. for ensembles with z = log p̄) and empirically contradicted on CIFAR | Rewritten: TS left digit-task detection essentially unchanged (≤ +0.012), shifted CIFAR-10 more visibly (up to +0.026), is not rank-preserving in general, and should be checked in the target setting | Theory + the measured heterogeneity | No | Manual |
| V4-04 | §4.6: "the pattern extended to every in-distribution metric, including ... ECE" without statistical qualification | §4.6 reports the CIFAR DeepEns-Snapshot ECE contrast explicitly: -0.0418, 95% CI [-0.0845, +0.0008], raw P=0.082 — directionally consistent but not statistically resolved at n=10; DeepEns-Single ECE -0.1805, P=0.0020; abstract and contributions scoped (NLL-anchored claim; mean ordering separated from statistical resolution) | reanalysis §7; the unresolved contrast is attributable to the collapsed replicate (drop-8: -0.0607, P=0.0039) | No | Number checks; LOO table in Deliverable B §8 |
| V4-05 | §4.6 noted "One of the ten replicates reversed the DeepEns-Snapshot ordering" with no cause | New §4.6 paragraph: the replicate's fresh restart (seed 10812) collapsed to uniform predictions within epoch 1 (train loss ≈ ln 10, logits → 0, accuracy ≈ 0.10) and never recovered — dead-network collapse under lr 0.1 without normalisation; verified by deterministic member-level re-run with the shared member reproducing bit-identically; replicate retained (no-exclusion rule); LOO sensitivity reported; practitioner-facing restart-risk reading added (ensemble still beat Single 0.929 vs 2.017) | `code/diagnose_seed8.py`; `results/v4/seed8_diagnosis.json` | No (diagnostic reproduction with identical seeds) | Deliverable C; gate on shared-member bit-identity |
| V4-06 | §3.5: OOD contrasts "reported uncorrected throughout" with no corrected OOD analysis defined anywhere | §3.5 now defines the OOD multiplicity framework: primary reporting = uncorrected exact P (as pre-specified); post-hoc robustness = Holm within each setting-probe-score family of 5 contrasts + setting-level + global sensitivities, labelled post-hoc with the definition date disclosed; Limitations repeats the labelling; §4.4 states the global-family caveat (nothing survives 55 tests, DeepEns included, because floor 0.0020 × 55 > 0.05) | Multiplicity-framework design; reanalysis families Oa/Ob/Oc | No | All families reported for every strategy (Table S4 + reanalysis JSON) |
| V4-07 | OOD results reported only for core + MNIST-direction settings (B=30, B=120, k=5 OOD unreported) | New Supplementary Table S4: all 11 setting-probe combinations × 3 vs-Single contrasts with Δ, 95% CI, raw P, Holm P; entropy-score summary in the caption | reanalysis (raw JSONL, all six settings) | No | Table generated programmatically |
| V4-08 | Fig. 4b caption: "SWA tracks Single throughout" | Softened to "stays closest to Single" | consistency with V4-01 | No | Visual QA |
| V4-09 | Practitioner guidance: "apply temperature scaling ... does no harm to shift detection" | Conditionalised: nearly free and repaired overconfidence in every condition here, but its effect on confidence-based shift scores is not guaranteed null (up to +0.026 AUROC on CIFAR-10) — verify in the target setting | same as V4-02/V4-03 | No | Manual |
| V4-10 | "Treat SWA as an accuracy-and-fit tool rather than a shift detector" (absolute) | "primarily as ... rather than a reliable shift detector"; Discussion mechanism paragraph adds that how much disagreement signal weight averaging discards is regime-dependent (CIFAR retained ~1/3 of the prediction-averaging gain) | CIFAR SWA +0.0247 result | No | Number check |
| V4-11 | Abstract: "Only prediction averaging ... " (see V4-01); abstract length must stay within IJMLC's 150-250 words | Abstract rewritten within the OOD/TS corrections and re-verified at exactly 250 words (excluding standalone math separators); v3 numbers preserved where correct | word-count script + PDF extraction | No | counted from compiled PDF |
| V4-12 | `download_data_cifar.py` printed per-channel means [0.329] — the script's own integrity check appeared to fail although the stored data are correct | Fixed to float64 aggregation with an explanatory comment (float32 sequential accumulation over 5.1e7 values drifts catastrophically) | direct verification: stored data match official statistics in float64; chunk-wise pixel equality vs the parquet source | No | verified this session |
| V4-13 | README one-sentence summary: "extends to out-of-distribution detection, where only prediction averaging helps" | Updated to the v4 claim form | same as V4-01 | No | manual |
| V4-14 | Checklist §7 ready-answer: "OOD AUROC TS-invariant within ±0.012" | Updated with the CIFAR caveat | same as V4-02 | No | manual |

## Title decision (re-reviewed in v4)

Kept: *"Deep ensembles outperform snapshot ensembles and weight averaging for
calibrated uncertainty under fixed training budgets"*. Rationale after the
v4 re-analysis: "outperform" is anchored on the primary outcome (NLL: the
ordering is significant in all six settings, all Holm P = 0.0098); the
secondary-metric exceptions (B=30/k=5 bounded reversals; the unresolved
CIFAR ECE contrast) are reported in the abstract, results and limitations,
so the title does not imply an all-metrics, all-scenarios claim. Rejected
alternatives remain documented in the v3 revision log (redundancy of
"budget-split...budgets"; question-style title).

## Numerical integrity checks performed on the v4 manuscript

- 34/34 automated checks pass (`code/verify_v4_numbers.py`): every number
  added in v4 is diffed against `results/v4/reanalysis_v4.json`, which was
  itself computed independently from the raw per-seed JSONL; the released
  analysis files reproduce exactly under this recomputation.
- All v3 numbers left unchanged in the text were re-verified in the v3
  session (100+ values, `verify_claims_v3.py`) and spot-re-verified now
  within the 34 checks.
- Table S4 was generated programmatically from the re-analysis JSON
  (`code/make_deliverable_b.py`); no manual transcription.
- Compile: 0 LaTeX errors; 0 overfull hboxes; 0 unresolved references;
  24 pages; abstract exactly 250 words; VLM visual QA on title page,
  CIFAR-results page and Table S4 page: PASS.
