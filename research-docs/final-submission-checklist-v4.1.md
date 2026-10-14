# Final Submission Checklist v4.1

**Manuscript:** v4.1.0 (14 October 2026) · **Target:** International
Journal of Machine Learning and Cybernetics (Springer)
**Guidelines source:** link.springer.com/journal/13042/submission-guidelines
(official page, accessed 14 October 2026)
**Companion documents:** revision-log-v4.1.md · claim-evidence-matrix-v4.1.md
· literature-positioning-v4.1.md · number-verification-v4.1.md

---

## 1. Guideline compliance (checked against the official page)

| Requirement | Guideline | v4.1 status |
|---|---|---|
| Abstract length | 150–250 words, no undefined abbreviations or unspecified references | 248 words; NLL/OOD/condition names defined at first use; no citations in abstract |
| Keywords | 4 to 6 | 6 keywords (unchanged) |
| Citation style | author and year in parentheses | natbib authoryear; all 28 entries cited (28/28 both directions) |
| Reference list | only works cited in the text | verified programmatically |
| Headings | decimal system, ≤ 3 levels | sections + subsections only |
| Declarations | required at submission via the interface: Author Contribution, Competing Interest | manuscript carries Declarations; **interface fields must be filled by the author at submission (P0 author action)** |
| LLM use | documented in Methods or a suitable alternative part; LLMs cannot be authors | AI-use disclosure present in Declarations; covers code, analyses, figures, initial draft and this revision; author accountability stated |
| Generative AI images | not used | none |
| Supplementary files | accepted | 4 supplementary figures + 4 tables in the same PDF (also acceptable); source data CSVs in the repository |
| LaTeX | accepted (.docx or LaTeX) | plain `article` class compiles cleanly with tectonic/LaTeX; production will supply the journal template — no conversion needed for submission |
| Title page | author names, affiliations, corresponding author, ORCID if available | present; **ORCID to be supplied by the author in the submission interface** |
| Data availability | expected | present; datasets public; per-replicate records in the repository |

## 2. Pre-submission problem list

### P0 — must be resolved before submission (all resolved in v4.1, none outstanding)

| Item | Status |
|---|---|
| Table 1 KMNIST s.d. row contradicted released records | **Fixed** (0.0116/0.0038/0.0084/0.0112); three-way cross-check |
| Abstract/contribution over-claimed the four-way ordering on the MNIST direction | **Fixed** (wording scoped; §4.2 and abstract now agree) |
| "by adjacency also SWA" inference | **Fixed** (direct contrast: −0.0176, CI [−0.0199,−0.0153], P=0.0020, all seeds agree) |
| Positioning paragraph internally inconsistent + outdated search window | **Fixed** (contrasts (i) acknowledged; re-check dated 14 Oct 2026) |
| Abstract over 250 words | **Fixed** (248) |

### P1 — strongly recommended before submission

| Item | Status / action |
|---|---|
| Author must fill submission-interface declaration fields (Author Contribution, Competing Interest, funding if any) and provide ORCID | Author action at submission time |
| Cover letter | Update the v4 cover letter to v4.1 (mention the corrected table row, the re-scoped abstract and the three new references); template in §6 |
| Brigato & Iocchi (2021) is an arXiv preprint | Acceptable; if a peer-reviewed version appears before submission, update the entry |
| ORCID for the corresponding author | Author action |

### P2 — improve if time allows

| Item | Status / action |
|---|---|
| Port to the Springer journal LaTeX template at production/revision stage | Not required for submission (generic article accepted); do only if the handling editor requests |
| Figure 5b could mark the collapsed replicate (seed 8) explicitly | Currently the anomaly is visible in panel (a) replicate dots; optional caption addition |
| README of the repository links the v4.1 release | Done in this revision's repository update |

### P3 — future research (documented, not blocking)

CIFAR-10-C corruptions; architectures with normalisation layers;
likelihood-based OOD scores; larger k; restart-failure rates at other scales.

## 3. New-experiment decision (Phase 7 of the directive)

**Question: without any new experiment, is the paper a defensible,
budget-matched empirical comparison study?** **Yes.** Reasons:

1. The primary result (NLL ordering under exactly matched budgets) is
   supported by five-contrast exact-permutation families in all six
   settings, with all-seed direction agreement, and replicates across
   architecture family and dataset modality.
2. Every secondary claim is now either supported at the stated level or
   explicitly bounded (CIFAR ECE contrast with CI and P; MNIST boundary
   condition; OOD family sensitivity; TS heterogeneity).
3. The 2024–2026 re-check found no study covering the checkpoint-matched
   prediction-vs-weight contrast for calibration/OOD endpoints, so the
   evidence base is not duplicated elsewhere.
4. The one new analysis this revision needed (the direct DeepEns–SWA
   contrast on MNIST) was computable from existing raw data.

**Recommended (not authorised) experiments, in priority order, if the
authors later choose to strengthen the paper:**

1. **A normalisation-layer replication (e.g., the same CNN with batch
   normalisation on CIFAR-10, B=60, k=3, 10 seeds).** Answers the most
   likely reviewer question about external validity ("does the SWA
   contrast survive BN?") and directly tests the documented limitation.
   Cost: ≈ 1,600 CPU epochs (~4 h on the study's hardware) + analysis;
   no new code paths beyond a flag. Risk: low (findings either way are
   publishable as boundary conditions). Not required for the current
   claims, which are already scoped to no-normalisation architectures.
2. **CIFAR-10-C corruptions as additional shift probes for the existing
   CIFAR checkpoints** (evaluation only, no retraining; the released
   records contain the trained weights' metrics, so this requires the
   stored checkpoints or a re-run at ≈ 1,600 epochs). Converts one
   dataset-level shift probe into a family; moderate reviewer appeal;
   medium cost; introduces probe-family multiplicity questions that would
   need pre-specification.

Neither is necessary for the present submission; both would belong to a
follow-up or a revision-if-requested cycle.

## 4. Reviewer-risk assessment (three most attackable points)

1. **Scale and architecture scope.** Two small networks, no normalisation
   layers, epoch-denominated budgets, small-scale image tasks. Mitigated
   by explicit scoping, the limitations section, and the conditional form
   of the practical rule; remains the top rejection risk regardless of
   wording.
2. **"Comparison paper, no new method."** Mitigated by the honest
   positioning (comparison design + boundary conditions + checkpoint-
   matched mechanism contrast), the verified absence of the
   checkpoint-matched contrast in the literature, and the three new
   citations that show the paper engages the 2022–2025 literature.
   The contribution is empirical and design-level; IJMLC publishes such
   studies, but fit is a judgement call for the editor.
3. **OOD multiplicity complexity.** The three-family presentation
   (uncorrected primary, per-probe Holm post-hoc, global sensitivity) is
   transparent but intricate; a reviewer may prefer a single family.
   Mitigated by the explicit statement that no conclusion depends on the
   family choice and that the global family kills everything including
   DeepEns (reported, not hidden).

## 5. Final submission judgement (Deliverable 6)

1. **Is v4.1.0 minimally complete for submission?** Yes — technically
   complete: version-locked source, verified numbers (232/241 automated
   checks + 9 documented dispositions), consistent figures/tables,
   guideline-compliant abstract/keywords/citations, honest declarations,
   reproducibility trail, clean compile (24 pp, 0 overfull, 0 undefined
   references).
2. **Is novelty still the biggest rejection risk?** Yes, together with
   scale (see §4). The paper does not propose a method; its value is the
   controlled design and the bounded empirical findings. The revision
   makes this as defensible as the evidence allows: claims that cannot
   survive the literature check are gone; the ones that remain are
   precisely scoped.
3. **Most persuasive evidence:** (i) the checkpoint-matched
   Snapshot–SWA contrast — a genuinely controlled mechanism separation
   replicated across 11 setting×probe combinations; (ii) the
   calibration-headroom boundary condition (MNIST vs Fashion-MNIST at
   the same budget); (iii) the budget-sweep direction (advantage grows
   with budget as the single network degrades); (iv) full raw-data
   transparency with bit-level reproduction gates.
4. **Three most attackable points:** as in §4 (scale; no new method;
   OOD multiplicity intricacy).
5. **New experiments or targeted revision?** Targeted revision
   (completed). The two recommended experiments (§3) are optional
   reinforcements, not gaps in the current claims.
6. **Must-fix before clicking submit:** fill the submission-interface
   declarations (author contribution, competing interest, funding if
   any), provide ORCID, attach the updated cover letter, and confirm the
   AI-use disclosure wording. Everything else in this checklist is done.

**Distinguish:** "manuscript is technically ready" (yes, modulo the
author-action items above) vs "high acceptance probability" (not
guaranteed — scale and novelty-fit remain editor/reviewer judgement
calls that wording cannot eliminate; the revision ensures the paper is
judged on its actual evidence, not on over-claims).

## 6. Cover letter skeleton (update from v4)

> Dear Editors,
> We submit "Deep ensembles outperform snapshot ensembles and weight
> averaging for calibrated uncertainty under fixed training budgets" for
> consideration in the International Journal of Machine Learning and
> Cybernetics. The study asks how a fixed training budget should be spent
> for calibrated uncertainty, comparing one long-trained network, budget-
> split deep ensembles, snapshot ensembles and stochastic weight
> averaging under exactly matched compute, paired seeds and (for the
> last two strategies) identical checkpoints. The primary finding —
> ordering on test NLL across budgets, ensemble sizes, both dataset
> directions and a CNN replication, with boundary conditions on
> near-saturated tasks and at the lowest budget — is reported with
> exact permutation inference, pre-registered core analysis, and all raw
> per-replicate records released. This revision (v4.1) corrects a
> standard-deviation row in one table, re-scopes two claims to match the
> statistical evidence, replaces an adjacency-based inference with a
> direct significant contrast, and adds three verified references from
> the 2021–2024 literature. We believe the study fits the journal's
> scope of machine-learning methodology with rigorous empirical
> evaluation. [Author to complete funding/COI sentences.]

## 7. Author-confirmation items (nothing below was invented)

- [ ] Author name, affiliation, email (kept as in v4.0.0: Chang Tan, Dalian
      University of Technology, aquars43@foxmail.com)
- [ ] ORCID to enter in the submission interface
- [ ] Funding statement (none is currently declared — confirm)
- [ ] Author-contribution text for the interface
- [ ] Competing-interest statement for the interface (manuscript says
      "none" — confirm)
- [ ] AI-use disclosure wording (extended in v4.1 to cover this revision —
      confirm it accurately describes the author's involvement)
- [ ] Choice whether to run the optional P3 experiments before or after
      submission (recommendation: submit now; hold experiments for
      revision-if-requested)
