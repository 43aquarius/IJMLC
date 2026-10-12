# IJMLC Submission Checklist v3 (Deliverable G)

Status: ✅ done · ⚠️ done with caveat · ☐ action for the author before submission
**Format compliance re-checked against the official IJMLC submission guidelines
on 12 October 2026** (Springer journal page 13042: abstract 150–250 words,
4–6 keywords, Statements and Declarations required at submission, editable
LaTeX source required, Springer Nature AI-disclosure policy applies).

## 1. Scientific content
- ✅ Research question in the first paragraph of Introduction and Abstract
- ✅ Contributions enumerated (6 bullets, including the cross-architecture replication)
- ✅ Related Work section with positioning paragraph and 2024–2025 re-check statement
- ✅ All claims bound to evidence; scope bounded in Abstract, Discussion, Conclusion
- ✅ Overclaim fixes verified: NLL/ECE-only ordering claim; B=30 secondary-metric
  exceptions quantified; B=30 post-TS reversal reported; SWA OOD wording
  ("no improvement surviving multiple-comparison correction")
- ✅ Boundary condition (MNIST saturation) reported prominently
- ✅ Statistical reporting: paired deltas, 95% CIs, exact permutation p, Holm
  families, resolution-floor note, preregistration vs post-hoc labelling
- ✅ Limitations section rewritten for two-architecture scope + inference cost
- ✅ Cross-architecture replication (CIFAR-10 + CNN) executed and integrated

## 2. IJMLC formatting
- ✅ Author–year citations (natbib authoryear, round); 24 references, alphabetical
- ✅ Abstract exactly 250 words (limit 150–250)
- ✅ Keywords: 6
- ✅ Conventional structure: Intro / Related work / Methods / Results / Discussion /
  Conclusion / Declarations
- ✅ Figures: 5 main (vector PDF) + 4 supplementary, per-panel CSV source data,
  self-contained captions
- ✅ Title page: author, affiliation, corresponding e-mail, date
- ☐ ORCID linked in the Editorial Manager profile (author action)
- ☐ Port to the official Springer `sn-jnl.cls` template when Editorial Manager
  requests source in the journal template (current article-class layout ports 1:1)
- ☐ Author-contribution + competing-interest fields filled in the submission
  interface (in addition to the in-manuscript Declarations)

## 3. Declarations & compliance
- ✅ Conflict of interest (none; sole author)
- ✅ AI-use disclosure retained and factual (workflow named; human direction and
  verification stated) — aligned with Springer Nature's generative-AI policy;
  note Springer retracted papers over *undeclared* AI use (Oct 2026), so the
  disclosure must remain in the submission
- ✅ Data availability (all four datasets public + cited; raw records released)
- ✅ Code availability (repo + release tag paper-v3.0.0)

## 4. Reproducibility package (github.com/43aquarius/IJMLC)
- ✅ Path-independent code (BME_ROOT override; no author-local directories)
- ✅ torchvision-free data pipeline; CIFAR via public HF mirrors with integrity checks
- ✅ Clean-environment gate verified: fresh venv + fresh data → 110/110 seed-0
  metric values bit-identical
- ✅ CIFAR sharded-execution resume equivalence verified bitwise
- ✅ Raw per-replicate records: 6 settings × 10 replicates (JSONL) incl. CIFAR
- ✅ Analysis outputs: analysis.json, analysis_v2.json, analysis_cifar.json (+ CSVs)
- ✅ Figure source data: 12 per-panel CSVs (incl. fig5a/b)
- ✅ Research documents: v2 + v3 audits, literature reviews (incl. 2024–2025
  re-check), experiment plans (incl. pre-specified CIFAR plan), revision logs,
  claim–evidence maps, simulated review, submission checklist

## 5. Pre-submission sanity checks (v3)
- ✅ 0 unresolved citations/references
- ✅ 0 LaTeX errors (overfull list re-checked after CIFAR table fill)
- ✅ Abstract ≤ 250 words
- ✅ Numerical integrity: 100+ v2 values re-diffed against analysis_v2.json (all
  PASS); CIFAR values inserted programmatically from analysis_cifar.json
- ✅ PDF watermark check: manuscript and release PDF verified free of viewer-added
  "AI-generated" stamps (4-layer verification documented in audit-report-v3.md)
- ☐ Final author read-through of Declarations and cover letter
- ☐ Cover letter updated with v3 title + CIFAR replication sentence

## 6. Cover letter (v3 draft)

> Dear Editors,
> I am submitting "Deep ensembles outperform snapshot ensembles and weight
> averaging for calibrated uncertainty under fixed training budgets" for
> consideration in the International Journal of Machine Learning and
> Cybernetics. The paper asks how a fixed training-compute budget should be
> allocated to obtain the best-calibrated predictive uncertainty, and answers
> it with a compute-exact four-way comparison (budget-split deep ensembles,
> snapshot ensembles, stochastic weight averaging, single long-trained
> network) in which the compared conditions share data, budget and, by
> construction, checkpoints. The design separates the two ingredients that are
> usually confounded—restarting versus continuing training, and combining in
> function space versus parameter space—and the conclusions are stress-tested
> across budgets, ensemble sizes, dataset directions, two OOD probes,
> per-condition temperature scaling, and a post-hoc replication on a
> convolutional network trained on CIFAR-10 with a natural-image shift probe.
> All code, per-replicate records and figure source data are public, and the
> pipeline reproduces the released records bit-for-bit from a clean
> environment. I believe this controlled empirical study fits the journal's
> scope on machine learning methodology with transparent evaluation, and I
> have no competing interests to declare. The experimental code, statistical
> analyses, figures and initial draft were produced with AI assistance under
> my direction; I specified the design, verified every number against the
> released records, and take full responsibility for the work.
> Sincerely, Chang Tan, Dalian University of Technology.

## 7. If reviews return: ready answers
- "Try a CNN / CIFAR-10" — **done in v3** (post-hoc-labelled replication; §4.6).
- "Corruptions?" — acknowledged as future work (Limitations); the
  checkpoint-matched template and released code make it mechanical.
- "Why is SWA weak on OOD?" — checkpoint-matched isolation + dense-SWA control
  + function-space vs parameter-space account (§5).
- "Is the gain just calibration?" — TS analysis (§4.3) with the B=30 boundary
  honestly reported; OOD AUROC TS-invariant within ±0.012.
- "10 seeds enough?" — exact permutation tests with Holm; resolution-floor note
  (§3.5); all per-seed data shown in figures.
- "Inference cost?" — four-dimension cost accounting (§3.1) and practitioner
  guidance (§5).
