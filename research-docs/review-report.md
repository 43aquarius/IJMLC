# Pre-submission review report

**Reviewer framework**: qinyan-nature-review (three lenses). Generated before delivery; all issues below refer to `paper/main.tex` (polished manuscript version).

## Review setup

- **Input scope**: full manuscript (abstract, introduction, results, discussion, methods, references, supplementary figures S1–S4 and supplementary tables S1–S2), figure source data, analysis outputs (`results/analysis.json`), analysis plan (`paper/research-design.md`) and figure contract (`paper/figure-contract.md`) were available for cross-checking.
- **Review boundary**: no re-training or new experiments were performed during review; numerical claims were checked against the released analysis outputs only. No journal-specific formatting policy was applied.
- **Central claim**: at a fixed training budget, budget-split independent restarts (DeepEns) give the best-calibrated uncertainty; weight averaging improves in-distribution metrics but shows no evidence of improving OOD detection.
- **Visible evidence**: Fig. 1 (6 panels), Tables 1–2, Supplementary Figs 1–4, Supplementary Tables 1–2, per-seed source data CSVs.

## Lens A — Conceptual significance

**Overall assessment**: the budget-matched framing is a genuinely practical contribution and the experiment is honestly scoped. The question ("how should a fixed budget be spent?") is the inverse of the usual method-vs-cost comparison and is directly actionable.

**Major strengths**
- The allocation question is concrete, falsifiable and practitioner-relevant; the four conditions isolate allocation, restart policy and combination mechanism in turn.
- The null result for SWA on OOD detection is a useful, non-obvious finding stated with appropriately calibrated language ("no evidence of improvement", CI crossing zero).

**Major concerns**: none.

**Minor concerns**
- A-M1 (P2): the title asserts "outperform ... for calibrated uncertainty"; supported for this regime, and the abstract states the boundary, but the title itself carries no scope qualifier.

**Not assessable**: editorial fit for any specific journal; novelty relative to the full literature (a systematic search was not performed during review).

## Lens B — Technical integrity

**Overall assessment**: the design, verification (bit-identity check, deterministic re-run), pre-registered analysis plan, and correct handling of the experimental unit (seed-level pairing) are well executed. The statistics match the recorded outputs.

**Major strengths**
- Independent unit = seed; all contrasts seed-paired; exact permutation tests with Holm correction on the pre-specified primary family; sensitivity analyses pre-specified; no exclusions.
- The entropy-score bug found during the study was fixed and the entire experiment re-run rather than patched post hoc; the deterministic pipeline reproduces recorded metrics exactly.

**Major concerns**
- B-M1 (P1, statistics-scope): the two OOD "no evidence" claims (SWA and SWA-dense AUROC vs Single) rest on n = 10 seeds and one OOD pair; the manuscript words these correctly as absence of evidence, but reviewers may still read them as evidence of absence. A power/precision statement for the null contrast (CI width already reported) would strengthen this.
- B-M2 (P1, baseline-fairness): no post-hoc calibration baseline (e.g., temperature scaling on the validation split) is included; the comparison therefore reflects uncalibrated deployment. The manuscript acknowledges this in the limitations, but a reviewer may ask whether the Single model with temperature scaling closes part of the NLL gap, which would sharpen the "what does ensembling buy beyond calibration" interpretation.

**Minor concerns**
- B-m1 (P2): the shared first member (DeepEns member 1 = Snapshot member 1) is well documented, but its effect on the DeepEns–Snapshot contrast (the difference is carried by members 2–3 only) could be stated even more explicitly where that contrast is interpreted.
- B-m2 (P2): wall-clock is reported per seed; total experiment energy/compute summary is not given (minor, increasingly expected).

**Not assessable**: correctness of the underlying PyTorch implementation beyond the deterministic reproduction check performed during the study.

## Lens C — Evidence and communication

**Overall assessment**: the claim–evidence mapping is tight; every quantitative claim in the text was checked against the analysis outputs and tables during this review and found consistent. Figures show all seed-level observations, satisfying the display standard.

**Major strengths**
- Numbers in abstract, text, tables and captions are mutually consistent (verified for NLL, ECE, AUROC, member NLL, JSD and SWA-dense contrasts).
- Calibrated verb strength throughout: "no evidence", "associated with", "we note ... associational"; no overclaim lexicon detected by the style audit (overclaim count 0).

**Major concerns**: none.

**Minor concerns**
- C-m1 (P2): Fig. 1 caption describes panel b as showing "the numbers above each condition give the mean (n = 10 seeds...)" — accurate; but the caption does not restate that SWA and Single differ in marker shape, relying on colour plus shape redundancy (this is present in the figure itself; caption could mention shape coding explicitly).
- C-m2 (P2): the term "cycle-end minima" appears in the figure contract but the final figure uses the label "snapshots θ1,θ2,θ3" only; the Methods text says "cycle end", consistent; no inconsistency remains, but a reader of the pre-registration and the figure side by side may look for the older wording.

## Cross-review synthesis

1. **Consensus strengths** (A + B + C): clean controlled design with pre-registration, deterministic reproducibility, honest null-result reporting, and full seed-level transparency in figures and source data.
2. **P0 consensus risks**: none identified.
3. **P1 consensus risks**:
   - `statistics-null-precision-01` (B-M1): precision/power framing for the two null OOD contrasts.
   - `baseline-posthoc-calibration-01` (B-M2): absence of a post-hoc calibration baseline.
   Both have clear, bounded resolution paths and do not undermine the central claim; they are future-work items rather than blocking defects, because the manuscript's wording is already calibrated ("no evidence") and the limitation is disclosed. Classification: P1 (important but with explicit repair path), not P0.
4. **Single-lens issues retained**: A-M1 (title scope qualifier), B-m1 (shared-member contrast wording), B-m2 (compute summary), C-m1/C-m2 (caption polish).
5. **Weight differences**: Lens B weights the null-claim precision most heavily; Lens C confirms the wording already guards against over-reading; hence P1 rather than P0.
6. **Minimal repair path** (applied to this manuscript before delivery where feasible):
   - Added an explicit CI-width sentence for the null contrasts (B-M1) → addressed in text.
   - Post-hoc calibration baseline (B-M2) → explicitly listed as future work in the limitations; not run (would require a new experiment and a validation-set protocol decision that belongs to the authors).
   - Title scope (A-M1) → kept as is; the abstract and discussion state the boundaries, and a scope-qualified title would exceed typical length conventions.
   - Caption shape-coding note (C-m1) → addressed in the Fig. 1 caption.
7. **Not assessable from current materials**: journal fit; peer-novelty relative to the complete 2024–2026 literature; authorship metadata (AUTHOR_INPUT_NEEDED in the manuscript).

## Issue ledger

Concern ID: B-M1
Issue key: statistics-null-precision-01
Severity: P1
Axis: statistics
Claim pointer: Results, OOD subsection ("SWA ... no evidence of improving OOD detection")
Evidence pointer: Table 2; Supplementary Table 2
Concern: the two OOD null contrasts rest on n = 10 seeds and one OOD pair; readers may over-read absence of evidence as evidence of absence.
Why it matters: over-strong null claims would not be supported by the design's precision.
Resolution test: text states the CI width for the null contrasts and retains "no evidence" wording (applied).

Concern ID: B-M2
Issue key: baseline-posthoc-calibration-01
Severity: P1
Axis: methods/baselines
Claim pointer: Discussion, practitioners paragraph (allocation rule)
Evidence pointer: NOT_PROVIDED (no temperature-scaling baseline was run)
Concern: without a post-hoc calibration baseline, the comparison reflects uncalibrated deployment only.
Why it matters: part of the NLL gap could in principle be closed by recalibrating the single model.
Resolution test: a future revision adds a temperature-scaled Single baseline; currently disclosed as a limitation (accepted, future work).

Concern ID: A-M1
Issue key: title-scope-01
Severity: P2
Axis: communication
Claim pointer: Title
Evidence pointer: Abstract boundary statement
Concern: title carries no scope qualifier.
Why it matters: minor risk of over-generalized reading.
Resolution test: scope is stated in the abstract and discussion; title kept within length convention (accepted).

Concern ID: B-m1
Issue key: shared-member-contrast-01
Severity: P2
Axis: methods
Claim pointer: Results, mechanism subsection (DeepEns-Snapshot interpretation)
Evidence pointer: Methods, budget-matched conditions
Concern: the DeepEns-Snapshot difference is carried by members 2-3 only because member 1 is shared.
Why it matters: precision of the mechanism interpretation.
Resolution test: clarifying clause added in the Results text (applied).

Concern ID: B-m2
Issue key: compute-reporting-01
Severity: P2
Axis: reporting
Claim pointer: Methods, reproducibility
Evidence pointer: wall-clock per seed values
Concern: total compute summary not stated.
Why it matters: reproducibility reporting completeness.
Resolution test: total-compute sentence added (applied).

Concern ID: C-m1
Issue key: caption-shape-coding-01
Severity: P2
Axis: figures
Claim pointer: Fig. 1 caption
Evidence pointer: Fig. 1 markers
Concern: caption does not mention marker-shape redundancy.
Why it matters: accessibility of the figure beyond colour coding.
Resolution test: caption text updated to mention shape coding (applied).

Concern ID: C-m2
Issue key: wording-consistency-01
Severity: P2
Axis: figures
Claim pointer: Fig. 1a label
Evidence pointer: Methods text
Concern: none remaining; earlier draft wording inconsistency resolved.
Why it matters: traceability between pre-registration and figure wording.
Resolution test: verified consistent in final manuscript (applied).

P0 issues: none. P1 issues: 2 (one addressed in text, one disclosed as future work). P2 issues: 5 (four addressed, one accepted).
