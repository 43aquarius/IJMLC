# IJMLC Submission Checklist v4 (Deliverable F)

Status: ✅ done · ⚠️ done with caveat · ☐ action for the author before submission
**Format compliance re-checked 13 October 2026** (Springer IJMLC guidelines:
abstract 150–250 words, 4–6 keywords, Statements and Declarations required,
editable LaTeX source, Springer Nature AI-disclosure policy).

## 1. Scientific content (v4)
- ✅ Research question in the first paragraph of Introduction and Abstract
- ✅ Contributions enumerated (6 bullets); OOD and TS bullets now carry the
  heterogeneity-reporting form (no absolute only-prediction-averaging claim)
- ✅ All claims bound to evidence; the claim–evidence matrix
  (`research-docs/claim-evidence-matrix-v4.md`) drives every v4 change
- ✅ v4 overclaim fixes: SWA-OOD "no improvement surviving correction"
  removed (contradicted by the paper's own data under the mirrored family);
  TS "at most +0.012" scoped to digit tasks; TS "ranking-invariant" theory
  claim removed; CIFAR ECE contrast reported as unresolved; anomalous
  replicate diagnosed and retained
- ✅ OOD multiplicity framework defined, post-hoc-labelled, and reported at
  three family sizes for every strategy (Table S4)
- ✅ Statistical reporting: paired deltas, 95% CIs, exact permutation P,
  Holm families, resolution-floor note, preregistration vs post-hoc
  labelling throughout
- ✅ Boundary condition (MNIST saturation) and restart-failure event reported

## 2. IJMLC formatting
- ✅ Author–year citations (natbib authoryear, round); 24 references,
  alphabetical
- ✅ Abstract exactly 250 words (counted from the compiled PDF, excluding
  standalone math separator glyphs)
- ✅ Keywords: 6
- ✅ Structure: Intro / Related work / Methods / Results / Discussion /
  Conclusion / Declarations + 5 main figures, 4 main tables, 4 supplementary
  figures, 4 supplementary tables (S1–S4)
- ✅ Compile: 0 errors, 0 overfull, 0 unresolved refs, 24 pages
- ☐ ORCID linked in the Editorial Manager profile (author action)
- ☐ Port to the official Springer `sn-jnl.cls` template when the journal
  requests source in its template
- ☐ Author-contribution + competing-interest fields in the submission
  interface

## 3. Declarations & compliance
- ✅ Conflict of interest (none; sole author)
- ✅ AI-use disclosure retained (workflow named; human direction and
  verification stated) — keep in the submission per Springer policy
- ✅ Data availability (four datasets public + cited; raw records released)
- ✅ Code availability (repo + release tag paper-v4.0.0)

## 4. Reproducibility package (github.com/43aquarius/IJMLC)
- ✅ Path-independent code; torchvision-free data pipeline; CIFAR via public
  HF mirrors with a now-correct float64 integrity check
- ✅ Raw per-replicate records: 6 settings × 10 replicates (JSONL)
- ✅ v4 additions: `results/v4/reanalysis_v4.json` (independent re-analysis
  with all OOD/TS families), `results/v4/seed8_diagnosis.json` (anomalous
  member diagnosis), `code/reanalysis_v4.py`, `code/diagnose_seed8.py`,
  `code/verify_v4_numbers.py` (34/34 checks), `code/make_deliverable_b.py`
- ✅ Research documents: v2–v4 audits, claim–evidence matrix v4, OOD/TS
  statistics report v4, CIFAR anomalous-seed report v4, revision logs,
  experiment plans, simulated review, submission checklists

## 5. Final submission advice (honest assessment)

**Resolved and no longer blocking.** The internal contradictions that a
careful reviewer with repository access would have found — the OOD
"only prediction averaging" claim vs. the CIFAR/B=30 SWA results in the
paper's own released data, and the TS "+0.012 on any condition" vs. the
CIFAR +0.026 — are fixed with the data now reported in full (Table S4).
The anomalous replicate is explained rather than unexplained variance, and
its handling follows the pre-specified no-exclusion rule with a labelled
sensitivity view. The statistical machinery independently reproduces.
None of these should now generate a credibility objection.

**Remaining reviewer-risk areas (ranked).**
1. **OOD probes are dataset-level shifts only** (no corruptions). The most
   likely substantive request; the limitation is stated and the template
   makes the extension mechanical. Not a validity threat to the claims as
   scoped.
2. **Small models / modest budgets.** Claims are explicitly bounded to the
   tested regime; risk is perceived narrowness, not over-claiming.
3. **SWA schedule restricted to 3 checkpoints** (checkpoint-matched by
   design); dense-SWA control + limitation statement cover it.
4. **One collapsed restart in 20** (CIFAR). Now reported with diagnosis and
   sensitivity; a reviewer may ask for more seeds — the permutation framework
   is already at its resolution floor for the primary contrasts, and the
   event works against, not for, the paper's preferred strategy.

**Is any further experiment necessary before submission?** No. Every change
in v4 is a re-analysis of existing raw data or a diagnostic reproduction
with identical seeds; no claim in the manuscript requires an unrun
experiment. The natural follow-ups (corruption benchmarks, BN/large-model
regimes, more restart-failure statistics) are stated as future work.

**Predicted review outcome.** Not attempted and not possible to guarantee.
The manuscript is at the standard expected of a well-controlled empirical
IJMLC submission: pre-registered core, seed-paired exact inference,
checkpoint-matched contrasts, full raw-data release, and claims that now
match the evidence in both direction and strength.

## 6. Cover letter (v4 draft)

> Dear Editors,
> I am submitting "Deep ensembles outperform snapshot ensembles and weight
> averaging for calibrated uncertainty under fixed training budgets" for
> consideration in the International Journal of Machine Learning and
> Cybernetics. The paper asks how a fixed training-compute budget should be
> allocated to obtain the best-calibrated predictive uncertainty, and answers
> it with a compute-exact four-way comparison (budget-split deep ensembles,
> snapshot ensembles, stochastic weight averaging, single long-trained
> network) in which the compared conditions share data, budget and, by
> construction, checkpoints. The design separates the two ingredients that
> are usually confounded—restarting versus continuing training, and combining
> in function space versus parameter space—and the conclusions are
> stress-tested across budgets, ensemble sizes, dataset directions, two OOD
> probes per direction, per-condition temperature scaling, and a post-hoc
> replication on a convolutional network trained on CIFAR-10 with a
> natural-image shift probe. Prediction averaging gave the largest and most
> consistent out-of-distribution gains; weight averaging of the same
> checkpoints showed smaller, task-dependent effects that the paper reports
> in full rather than summarising categorically. All code, per-replicate
> records and figure source data are public, the pipeline reproduces the
> released records from a clean environment, and every statistical claim was
> re-derived independently from the raw per-seed data before this submission.
> I believe this controlled empirical study fits the journal's scope on
> machine learning methodology with transparent evaluation, and I have no
> competing interests to declare. The experimental code, statistical analyses,
> figures and initial draft were produced with AI assistance under my
> direction; I specified the design, verified every number against the
> released records, and take full responsibility for the work.
> Sincerely, Chang Tan, Dalian University of Technology.

## 7. If reviews return: ready answers (v4)
- "Try a CNN / CIFAR-10" — done (post-hoc-labelled replication; §4.6).
- "Corruptions?" — acknowledged future work (Limitations); template + code
  released; the OOD claims are scoped to the dataset-level shifts tested.
- "Why is SWA's OOD effect inconsistent?" — §4.4 now reports it as small and
  task-dependent (-0.016..+0.025) with the checkpoint-matched separation
  (Snapshot−SWA significant everywhere on NLL/OOD in the core and CIFAR
  settings); the mechanism account is associational.
- "Is the gain just calibration?" — TS analysis (§4.3) with the B=30 boundary
  and the CIFAR TS-OOD shifts (+0.026 Single) reported; TS is not
  rank-preserving in general.
- "10 seeds enough?" — exact permutation tests with Holm; resolution-floor
  note (§3.5); all per-seed data shown in figures; leave-one-out sensitivity
  for the CIFAR anomalies in Supplementary Table S4 / Deliverable B.
- "The anomalous CIFAR replicate?" — §4.6 diagnosis (collapsed fresh restart,
  verified by deterministic re-run), retained under the no-exclusion rule,
  sensitivity reported; unique among 20 fresh restarts.
- "Inference cost?" — four-dimension cost accounting (§3.1) and practitioner
  guidance (§5).
