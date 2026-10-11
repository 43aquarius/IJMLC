# IJMLC Submission Checklist (Deliverable G)

Status: ✅ done in v2 · ⚠️ done with caveat · ☐ action for the author before submission

## 1. Scientific content
- ✅ Research question stated in first paragraph of Introduction and Abstract
- ✅ Contributions enumerated as a bullet list (Introduction)
- ✅ Related work section separate (§2), positioning paragraph included; no overclaim of
  algorithmic novelty ("comparison design and measurement")
- ✅ All claims bound to evidence; scope bounded in Abstract, Discussion and Limitations
- ✅ Boundary-condition result (MNIST saturation) reported rather than buried
- ✅ Statistical reporting: paired deltas, 95% CIs, exact permutation p, Holm families;
  preregistration status of core vs. extensions labelled
- ✅ Limitations section with 8 specific items incl. architecture, modality, budget units,
  SWA schedule, single calibrator, probe type, associational mechanism
- ⚠️ Architecture scope: MLP-only — reviewers may still push back; the Limitations section
  frames it as CPU-bound scope and provides the reusable template for extensions

## 2. IJMLC formatting conventions
- ✅ Author–year citations (natbib authoryear, round)
- ✅ References alphabetically ordered by first author surname
- ✅ Abstract 239 words (IJMLC range 150–250)
- ✅ Keywords: 6 (deep ensembles; snapshot ensembles; SWA; uncertainty calibration;
  budget-matched evaluation; OOD detection)
- ✅ Conventional structure: Intro / Related work / Methods / Results / Discussion /
  Conclusion / Declarations
- ✅ Figures: 4 main (vector PDF), each with per-panel CSV source data; captions self-contained
- ☐ Port to the official Springer `sn-jnl.cls` template when the Editorial Manager asks for
  source in the journal template (v2 uses a clean article-class layout that ports 1:1; the
  cover letter can note this)
- ☐ ORCID linked in the submission system; final affiliation details (school/department within
  Dalian University of Technology) if desired

## 3. Declarations & compliance
- ✅ Conflict of interest declared (none; sole author)
- ✅ AI-use disclosure (factual; names the workflow; states human direction and verification)
- ✅ Data availability (public datasets; raw records released)
- ✅ Code availability (GitHub repo + release tag)
- ☐ Cover letter (draft below)

## 4. Reproducibility package (all in github.com/43aquarius/IJMLC)
- ✅ Code: run_experiments_v2.py + common.py + analyze_v2.py + make_figures_v2.py (+ v1 scripts)
- ✅ Raw per-replicate records: 5 settings × 10 replicates (JSONL)
- ✅ Analysis outputs: analysis_v2.json, summary_v2.csv, contrasts_v2.csv
- ✅ Figure source data: 7 v1 CSVs + 5 v2 CSVs (one per panel)
- ✅ Determinism evidence: bit-level reproduction of v1 by v2 (28/28 metrics, seed 0)
- ✅ Research documents: audit, literature review, experiment plan, revision log, claim–evidence
  map, figure contract, review report

## 5. Pre-submission sanity checks (last pass)
- ✅ 0 unresolved citations/references in compiled PDF
- ✅ 0 overfull hboxes
- ✅ 19 pages incl. supplementary; fonts embedded (tectonic default)
- ✅ VLM visual QA passed on title page, 2 results pages, references page, all 3 new figures
- ✅ Numerical spot-check: 12 headline numbers verified present and matching analysis JSON
- ☐ Final read-through by the author (especially Declarations wording)

## 6. Suggested cover letter (draft)

> Dear Editors,
> I am submitting "Budget-split deep ensembles outperform snapshot ensembles and weight
> averaging for calibrated uncertainty" for consideration in the International Journal of
> Machine Learning and Cybernetics. The paper asks how a fixed training-compute budget should
> be allocated to obtain the best-calibrated predictive uncertainty, and answers it with a
> compute-exact four-way comparison (budget-split deep ensembles, snapshot ensembles,
> stochastic weight averaging, single long-trained network) in which the compared conditions
> share data, budget and, by construction, checkpoints. The design separates the two
> ingredients that are usually confounded—restarting versus continuing training, and
> combining in function space versus parameter space—and the conclusions are stress-tested
> across budgets, ensemble sizes, dataset directions, two OOD probes and per-condition
> temperature scaling. All code, per-replicate records and figure source data are public.
> I believe this controlled empirical study fits the journal's scope on machine learning
> methodology with transparent evaluation, and I have no competing interests to declare.
> Sincerely, Chang Tan, Dalian University of Technology.

## 7. If reviews return: likely asks and ready answers
- "Try a CNN / CIFAR-10": acknowledged as primary future work (Limitations); the paired-seed
  template and released code make the extension mechanical.
- "Why is SWA weak on OOD?": checkpoint-matched isolation shows it is the combination
  mechanism, not the trajectory; dense-SWA control (Suppl. S2) rules out the number of
  averaged checkpoints; discussion §5 gives the function-space vs parameter-space account.
- "Is the gain just calibration?": TS analysis (§4.3) shows the ordering survives
  per-condition recalibration and OOD AUROC is TS-invariant; both points in the text.
- "Sample size of 10 seeds": exact permutation tests with Holm correction; all per-seed data
  shown; CIs reported for every contrast.
