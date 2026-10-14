# Revision Log v4.0.0 → v4.1.0

**Manuscript:** "Deep ensembles outperform snapshot ensembles and weight
averaging for calibrated uncertainty under fixed training budgets"
**Base:** tag `paper-v4.0.0` (commit 52b7751c, immutable)
**Revision date:** 14 October 2026
**Verification basis:** full independent recomputation of every checked
number from the raw per-seed JSONL records (`scripts/verify_v41_stage1.py`,
`..._stage2.py`, `..._stage3.py`, preserved in the repository), a fresh
literature re-check through 14 October 2026, and the IJMLC official
submission guidelines (link.springer.com/journal/13042/submission-guidelines,
accessed 14 October 2026).

**What this revision is not:** no experiment was re-run, no data were added
or removed, no result was recomputed into a different value except where the
v4.0.0 manuscript printed a number that contradicted its own released
records (one table row, fixed below). All ten seeds, including the collapsed
CIFAR replicate 8, are retained in all analyses.

---

## 1. Core modification list (Deliverable 2 format)

| # | Location | Original problem | Specific modification | Basis | Affects conclusion? | Verification status |
|---|----------|------------------|-----------------------|-------|---------------------|---------------------|
| 1 | Table 1, KMNIST-probe row | s.d. values (0.0184/0.0067/0.0131/0.0132) contradicted the released records; means were correct | Corrected to 0.0116/0.0038/0.0084/0.0112 (Single/DeepEns/Snapshot/SWA) | Independent recomputation from `results/v2/experiment_v2_fmnist_B60_k3.jsonl`; matches `analysis_v2.json` and `source-data/fig4b_ood_overview.csv`. Wrong values first appeared in v2 and propagated to v4 | No (display-only; all contrast CIs/P values involve paired differences and were already correct) | Recomputed and cross-checked 3 ways; rendered value verified in compiled PDF |
| 2 | Abstract; contributions bullet 2 | "The ordering was robust across … a reversed dataset direction" overstated: on MNIST the four-way mean ordering does not hold (SWA mean NLL 0.0741 > Single 0.0724; SWA mean ECE 0.0101 > Single 0.0098); only the DeepEns-vs-all comparisons are supported there | Abstract rewritten: ordering claim now scoped to budgets/ensemble sizes/CIFAR; MNIST stated as "only DeepEns separated from Single; single-trajectory strategies showed no reliable improvement". Bullet 2 rewritten identically ("lowest mean test NLL in every setting; four-way ordering held on NLL across budgets, ensemble sizes and CIFAR-10; on MNIST … not in evidence") | Raw per-seed recomputation (MNIST setting, 10 seeds); §4.2 of v4 already scoped the claim correctly to Fashion-MNIST settings — the abstract/bullet now match it | Clarifies, does not weaken: DeepEns is significantly best on MNIST vs every alternative (see #4) | Recomputed; PDF text verified |
| 3 | Abstract; §4.6 cross-reference | Abstract did not state that the CIFAR DeepEns–Snapshot ECE advantage is not statistically resolved (−0.0418, CI [−0.0845, +0.0008], P=0.082) | Added "where the DeepEns–Snapshot calibration-error advantage was directionally consistent but not statistically resolved" to the abstract; bullet 2 states it too | Recomputed ECE contrast (exact sign-flip P=0.0820) | No (§4.6 already reported the contrast honestly; abstract now consistent) | Recomputed; PDF text verified |
| 4 | §4.2 (reversed dataset direction) | "and by adjacency also SWA" transferred significance between adjacent contrasts | Replaced with a direct post-hoc contrast: DeepEns−SWA on MNIST NLL −0.0176, 95% CI [−0.0199, −0.0153], uncorrected exact P=0.0020, all ten seeds agreeing in direction; explicitly labelled a post-hoc check outside the five-contrast family | Newly computed from raw records (this is a re-analysis of existing data, not a new experiment) | Strengthens (the direct test is significant; inference no longer borrowed) | Recomputed; PDF text verified |
| 5 | Related Work, Positioning paragraph | Internal inconsistency: text acknowledged Ashukha et al. (2020) do compute-matched single-vs-ensemble comparisons while claiming a re-check "did not surface a study covering **any** of these three contrasts"; search window outdated ("2024–2025") | Rewritten: contrast (i) acknowledged as partially covered (Ashukha in-domain; Brigato & Iocchi under architecture scaling; Ramé et al. for OOD generalisation; Ajroldi et al. for acceleration); novelty claimed for the checkpoint-matched contrast (ii), the joint design (iii), and the comparison design; re-check date stated (searches through 14 October 2026, emphasising 2024–2026) | Fresh literature re-check this session (14 web searches + arXiv API + OpenReview API + publisher DOI checks); Ashukha content verified from the paper's own abstract (DEE score) | Positions the paper honestly; prevents a reviewer catching the inconsistency | Every new citation verified against a primary source |
| 6 | Related Work (three additions) | Missing directly relevant prior work found in the re-check | Added: Brigato & Iocchi (2021, arXiv:2111.14493) — budget-matched ensemble-vs-single with architecture scaling; Ramé et al. (2022, NeurIPS) — DiWA, weight averaging for OOD *generalisation*; Krumpl et al. (2024, WACV) — adaptive temperature scaling improves OOD *detection* | Titles/authors/venues verified (arXiv API, proceedings.mlr.press v267 for Ajroldi re-check, openaccess.thecvf.com for ATS, NeurIPS 2022 for DiWA) | No (positions, does not change findings); ATS citation directly supports the TS-OOD claim | All verified this session |
| 7 | §4.3 (temperature scaling) | The TS-changes-OOD finding lacked literature anchoring | Appended "adaptive, sample-specific temperature scaling exploits exactly this freedom to improve OOD detection \citep{krumpl2024}" and a corresponding sentence in Related Work | Krumpl et al. WACV 2024 (verified from the paper PDF) | No | PDF first page read and verified |
| 8 | §4.4 (OOD) | "this difference is attributable to the combination mechanism alone: averaging predictions **transfers** the members' ability…" stated a mechanism reading as fact | Rewritten: "this difference reflects only how the checkpoints are combined. A reading consistent with the member-level measurements is that averaging predictions preserves the members' disagreement…" | Design fact (identical checkpoints) kept; mechanism story explicitly marked as a reading | No (wording precision) | Manual review |
| 9 | §4.4 | "Holm-adjusted P ≤ 0.031" rounding error (actual max 0.0312) | "≤ 0.032" | Recomputed Holm values (MNIST-direction FMNIST-probe family) | No | Recomputed |
| 10 | Discussion (opening) | "these differences are attributable to the allocation of the budget and the mechanism of combination rather than to tuning or **trajectory noise**" — the trajectory continuation IS the treatment for DeepEns–Snapshot; "trajectory noise" is excluded only for Snapshot–SWA | Split into two precise statements: differences reflect budget allocation and combination rule rather than tuning/data; Snapshot–SWA difference specifically is free of run-to-run variation | Design logic | No (removes an over-broad causal claim) | Manual review |
| 11 | Introduction; §4.5 | "isolates the effect…", "with no trajectory noise" (Intro); "the design also pins down why" (§4.5) — causal overreach flags | Intro: "measures what restarting training independently buys over continuing one trajectory… no run-to-run variation between the two conditions"; §4.5: "yields two measurable ingredients that separate DeepEns from Snapshot" | User audit instruction 6.5 (causal language must match control level) | No | Manual review |
| 12 | §3.5 (statistics) | "as pre-specified" attached to the OOD uncorrected reporting could be read as claiming a pre-registered OOD family | "consistent with the pre-specified plan, under which formal correction applies to the NLL families only" | Pre-registration (`research-docs/research-design.md` §5.3) verified: correction covers NLL only; secondaries are effect estimates | No (more precise, same substance) | Pre-registration re-read |
| 13 | §3.3 (training) | Wall-clock "72–87 s" did not match the records (70.6–86.1 s) | "71–86 s" | Recomputed from `results/experiment.jsonl` wallclock_s fields | No | Recomputed |
| 14 | Declarations | AI-use disclosure covered the initial draft but not the revision workflow | Extended: "…the initial manuscript draft **and the present revision**…"; consistent with Springer's LLM policy (documented in Methods or a suitable alternative part — Declarations here) | IJMLC submission guidelines (accessed 14 Oct 2026) | No | Guideline text extracted and checked |
| 15 | Code availability | Pointed at `paper-v4.0.0` | `paper-v4.1.0` | Release created with this revision | No | Release asset MD5-verified |
| 16 | Abstract | v4 abstract was 251+ words; after the accuracy edits it reached 279 — over the official limit | Rewritten to 248 words (limit 150–250), preserving all required content: research question, four strategies, core NLL result, ECE boundary, OOD task dependence, TS effect + exceptions, post-hoc labels, scope statement | IJMLC guidelines (150–250 words) | No | Word count verified programmatically |
| 17 | Bibliography | 25 bibitems but `thebibliography{24}` width hint; 3 new references added | `{28}`; three new verified entries inserted in alphabetical order; all 28 entries cited in text (28/28 both directions) | Citation consistency check | No | Programmatic check |

**Total: 17 tracked modifications, of which #1 is a data-display correction
(P0), #2–#5 are claim-accuracy corrections (P0/P1), #6–#7 are literature
completions (P1), #8–#12 are causal/statistical-language tightenings (P1),
#13–#17 are compliance and polish (P2).**

## 2. Items checked and found correct (no change)

All of the following were independently recomputed from the raw per-seed
records and matched the v4.0.0 manuscript exactly (see
`number-verification-v4.1.md` for the full table):

- Table 1 (core summaries; 34 of 38 cells — the four KMNIST s.d. cells were
  the exception, fixed above), Table 2 (all five NLL contrasts with CIs and
  Holm P), Table 3 (extension contrasts), the CIFAR table (24 cells + 5
  contrasts), Supplementary Tables S1 (25 contrasts), S2 (SWA-dense), S3
  (TS-NLL contrasts), S4 (33 OOD contrasts with uncorrected and Holm P).
- All in-text statistics: budget sweep values, B=30/k=5 secondary-metric
  exceptions, member-level measurements (member NLL/accuracy/JSD in core,
  k=5 and CIFAR), fitted temperatures (core and CIFAR), TS effects on OOD
  AUROC per condition (digit max +0.0119; CIFAR +0.0035…+0.0260), the CIFAR
  gap compression +0.069 → +0.046, SWA OOD effect ranges and significance
  counts (5 positive / 1 negative / 5 null of 11), DeepEns 11/11 and
  Snapshot 9/11 OOD family significance, entropy-score range −0.0147…+0.0306.
- The anomalous-replicate account (replicate 8: ensemble NLL 0.929, ECE
  0.2095, member accuracy 0.5146, JSD 0.3288; Snapshot 0.882; Single 2.017;
  leave-one-out sensitivities −0.2075 / −0.0607 at P=0.0039; uniqueness of
  the DE–SN reversal across the ten replicates) and the diagnosis in
  `results/v4/seed8_diagnosis.json` (member 2 collapse: train loss ≈ ln 10
  from epoch 1, logits → 0, accuracy ≈ 0.10, never recovers).
- v1↔v2 record bit-consistency (200/200 comparisons over 10 seeds × 4
  conditions × 5 metrics); the ECE/NLL mean orderings on all five
  Fashion-MNIST settings and CIFAR; B=120 strict every-metric ordering
  claim; the reliability-diagram claim (mean confidence 0.9595 vs mean
  accuracy 0.8895); epoch accounting (1,600 + ~8,880 + 1,600; dense-SWA
  re-run documented); the ~69-minute extension total (68.9 min).

## 3. Items left unchanged after explicit consideration

- **Title.** "outperform … for calibrated uncertainty" remains anchored on
  the primary outcome (NLL), with the secondary-metric boundaries stated in
  the abstract, contributions, results and conclusion. Alternatives
  considered and rejected (documented in the v3/v4 revision logs): any title
  that enumerates the scope ("…under fixed training budgets in small-scale
  image classification") is longer without being more accurate, since the
  budget condition is already in the title and the scope statement is in
  the abstract.
- **The pre-registration boundaries** as stated in §3.5 (core plan stored
  before any test evaluation; n=5→10 amendment after timing pilot, before
  outcomes; extensions and TS and CIFAR labelled post-hoc; OOD families
  labelled post-hoc with definition date disclosed).
- **The four-cost-dimensions paragraph** (§3.1) separating training budget,
  wall-clock, inference cost and deployment cost — unchanged and verified
  against instruction 7.4.
- **All figures** (fig1–fig5, suppl figs 1–4) — unchanged; their source
  data CSVs match the corrected statistics (the KMNIST s.d. correction
  brings Table 1 into agreement with `source-data/fig4b_ood_overview.csv`,
  which was already correct).
- **Author block, declarations of interest, data availability** — author
  facts (name, affiliation, email, ORCID at submission) require author
  confirmation and were not touched.

## 4. Compilation and verification gate

- `tectonic main_v4_1.tex` compiles cleanly: 24 pages (same as v4.0.0),
  0 overfull boxes, 0 undefined references/citations, 28/28 bibliography
  entries cited both directions.
- Every passage modified in this revision was located in the compiled PDF
  text and checked to render as intended.
- Abstract word count 248 (programmatic count; guideline limit 250).
- Key figures/tables cross-references intact (no new labels; no removed
  labels).
- The v4.0.0 baseline (tag `paper-v4.0.0`, commit 52b7751c) is untouched;
  v4.0.0 files (`manuscript-source/main.tex`, all released PDFs) remain
  retrievable from that tag.
