# Research Audit Report (Deliverable A)

**Manuscript:** "Budget-split deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty"
**Target journal:** International Journal of Machine Learning and Cybernetics (IJMLC)
**Audit date:** 11 October 2026 (session 2)
**Auditor roles:** ML researcher / IJMLC reviewer / literature researcher / statistics & experiment auditor / English editor

---

## 1. Answers to the seven framing questions

**Q1. What is the most valuable contribution of the paper?**
The fully budget-matched, checkpoint-matched four-way design itself. Two contrasts are unusually clean by construction: (i) DeepEns–Snapshot isolates "independent restarts vs. continued trajectory" because both ensembles share member 1 bit-identically; (ii) Snapshot–SWA isolates "prediction averaging vs. weight averaging" because both consume the *identical* three checkpoints. Prior benchmark studies vary budgets across methods; this design holds compute, data, optimizer and pairing constant. The OOD finding (only prediction averaging improves shift detection; weight averaging shows no evidence of improvement) is the most novel empirical nugget.

**Q2. What conclusions are actually supported?**
- (a) At B=60 epochs on this task, all three strategies beat Single on NLL with tight paired CIs (Holm-adjusted p=0.0098).
- (b) Strict ordering DeepEns > Snapshot > SWA on every in-distribution metric measured.
- (c) SWA shows no evidence of improved MSP/entropy AUROC (CI [−0.017, +0.011]).
- (d) Member-level association: restarts have better-calibrated members (NLL 0.338 vs 0.404) *and* higher diversity (JSD 0.0150 vs 0.0106).

**Q3. Which conclusions are too broad?**
None stated beyond the evidence — the manuscript repeatedly bounds claims to "small networks, one dataset family, one shift type". This honesty is a strength. (The v1 claims were audited for overclaim: style audit found 0 booster terms.)

**Q4. Which contributions are already covered by prior work?**
- Ashukha et al. (ICLR 2020) already compared single long-trained models vs. ensembles under matched-compute framing ("pitfalls of in-domain uncertainty estimation") — our DeepEns-vs-Single contrast partially overlaps their single-vs-ensemble analysis. **Differentiators:** they did not include snapshot ensembles or the checkpoint-matched SWA contrast; our shared-first-member and identical-checkpoints construction is tighter than anything in their design.
- Fort et al. (2019) established the diversity/init mechanism for ensembles at unconstrained budget; our member-level analysis replicates their intuition *under budget constraint*. The paper already cites both; the Related Work must position against them explicitly (currently implicit).
- The "ensembles improve OOD detection" observation exists in the literature (e.g., Lakshminarayanan et al. 2017; Ovadia et al. 2019); our specific novel element is that *weight averaging of the same checkpoints* does not, which to our knowledge is not isolated elsewhere.

**Q5. Which defects most affect acceptance at IJMLC?**
1. Single-dataset-family evidence (P1) — the #1 reviewer complaint for any empirical ML paper.
2. No post-hoc recalibration baseline (temperature scaling) — the standard "but did you try TS?" rejection vector (P1).
3. Citation-format non-compliance and, worse, **broken citation numbering** (P0, see below).
4. Nature-style formatting (Results-before-Methods, superscript numeric citations) instead of IJMLC conventions (author-year, separate Related Work section).

**Q6. What can be achieved by rewriting alone?**
Citation system repair, IJMLC reformatting, Related Work section, positioning, author metadata, declarations. Estimated ~60% of the gap to a competitive submission.

**Q7. Which additional research is most worth the compute?**
In order of value per CPU-hour: (1) reverse dataset direction (MNIST in-distribution); (2) additional OOD probe (KMNIST); (3) temperature-scaling baseline (needs no retraining — fits into evaluation); (4) budget sweep (B=30, B=120); (5) ensemble size k=5; (6) larger architecture (CPU-infeasible at full grid; deferred honestly).

---

## 2. P0–P3 issue register

Priorities: **P0** = blocking correctness/compliance; **P1** = likely reviewer rejection vector; **P2** = weakens paper; **P3** = polish.

| ID | Priority | Location | Issue | Root cause | Fix applied in v2 | Needs experiment |
|----|----------|----------|-------|------------|-------------------|-----------------|
| A-01 | **P0** | Methods §Datasets: "MNIST\textsuperscript{19}" | Text cites [19]; bibliography ends at [18]. MNIST (LeCun et al. 1998) is entry 18, so its in-text number points past the list. | Manual superscript numbers instead of `\cite` | Full author-year rewrite with `\citep{}` — numbering eliminated as a failure mode | No |
| A-02 | **P0** | Methods §Datasets: "Fashion-MNIST\textsuperscript{18}" | Dataset citations off by one: xiao2017 is bibitem 17, not 18 | Same | Same | No |
| A-03 | **P0** | Intro ¶1: snapshot ensembles "…\textsuperscript{2,14}" | [14] is Nguyen et al. "easily fooled" — irrelevant to snapshot ensembles; intended SGDR (loschchilov2017, [4]) | Manual numbering drift | Author-year rewrite | No |
| A-04 | **P0** | Intro ¶1: "…uncertainty quantification\textsuperscript{16,17}" | [17] is the Fashion-MNIST dataset paper, not a UQ reference | Manual numbering drift | Author-year rewrite | No |
| A-05 | **P0** | Title block | Author information missing ("pending author confirmation") | Info unavailable at v1 time | Author added: Chang Tan, Dalian University of Technology, sole & corresponding author, aquars43@foxmail.com | No |
| A-06 | **P0** | Title block / repo | AI-assistance disclosure absent; workflow branding text in title block mixes promotional and factual content | v1 pipeline limitation | Formal AI-use declaration in Declarations; workflow text removed from title page; AI involvement still fully disclosed | No |
| A-07 | **P1** | Whole paper | Single dataset family (FMNIST-ID / MNIST-OOD) | v1 scope | **E-B: MNIST-ID direction added (10 seeds)** + KMNIST as second OOD probe in all settings | **Yes** |
| A-08 | **P1** | Whole paper | Single shift type | v1 scope | **KMNIST probe added everywhere** (harder, character-level shift) | **Yes** |
| A-09 | **P1** | Discussion ¶5 (limitation) | No post-hoc recalibration baseline; TS explicitly named as not applied | v1 scope | **Temperature scaling fitted per condition on validation, reported for all settings** | **Yes** |
| A-10 | **P1** | Whole paper | Single budget (B=60) | v1 scope | **E-C (B=30) and E-D (B=120) added, 10 seeds each** | **Yes** |
| A-11 | **P1** | Whole paper | Single ensemble size (k=3) | v1 scope | **E-E: k=5 added (DeepEns-5/Snapshot-5/SWA-5), 10 seeds** | **Yes** |
| A-12 | **P1** | Formatting | Nature-style: superscript numeric citations, Results-first, no Related Work section; IJMLC uses author-year, alphabetical references, conventional IMRaD + Related Work, 150–250-word abstract, 4–6 keywords | v1 written for a generic preprint style | Full restructure to IJMLC conventions | No |
| A-13 | **P2** | Methods §Reproducibility: "about 13 minutes per seed" | Factually wrong: measured wall-clock is ~76 s/seed (13 min was the whole 10-seed run) | Transcription slip in v1 | Corrected with actual timings from v2 logs | No |
| A-14 | **P2** | References | Journal names in Nature abbreviation style ("Adv. Neural Inf. Process. Syst."); IJMLC/Springer expects full names or its own style | v1 style | Springer-style reference formatting, alphabetical order | No |
| A-15 | **P2** | Data availability | No repository URL given | Repo created after v1 | github.com/43aquarius/IJMLC cited; release-linked PDF | No |
| A-16 | **P2** | Abstract | 249 words, single paragraph, no keywords; IJMLC wants 150–250 words + 4–6 keywords | v1 style | Rewritten abstract within limits; 6 keywords added | No |
| A-17 | **P2** | Whole paper | MLP-only architecture | CPU feasibility | Deferred honestly as limitation + future work (stated, not hidden) | Would need GPU |
| A-18 | **P3** | Title block date | "22 September 2026" stale | — | Updated | No |
| A-19 | **P3** | Fig. 1 caption | Caption is long and self-contained (good) but condition names rely on colour+shape; verified OK in v1 VLM audit | — | Kept; minor copyedits | No |
| A-20 | **P3** | Repo README | Citation block has placeholder author "43aquarius" | Author now known | Updated to Chang Tan | No |

**Reproducibility anchor:** the v2 pipeline reproduces v1 exactly — seed 0 re-run under v2 code matched **28/28 recorded metrics bit-for-bit** (same torch 2.14.0+cpu, same seeds, shared-first-member bit-identity check passed).

---

## 3. Statistical audit (12 items, deliverable D-audit component)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | Pairing respected in all analyses | PASS | All contrasts are within-seed paired differences; analysis.json stores per-seed deltas |
| 2 | Seed is the unit of replication | PASS | n=10 per condition; no member- or sample-level pseudoreplication anywhere |
| 3 | Paired difference + 95% CI reported | PASS | t-interval df=9; CIs in contrasts.csv |
| 4 | Exact sign-flip permutation tests | PASS | All 2^10 sign patterns enumerated; p=0.0020 floor = 2/1024 consistent with n=10 |
| 5 | Holm correction on primary family | PASS | 5 contrasts on NLL; adjusted floor 0.0098 |
| 6 | Primary vs. secondary metrics separated | PASS | NLL primary; acc/Brier/ECE/AUROC labelled secondary/uncorrected |
| 7 | Exploratory analyses labelled | PASS | SWA-dense, sensitivity analyses flagged exploratory/uncorrected |
| 8 | Direction/sensitivity checks | PASS | ECE-10 and entropy-AUROC replicate all signs (v1 verified) |
| 9 | No test-set peeking before analysis plan | PASS | Plan written pre-test-eval; only amendment (5→10 seeds) made after timing pilot, documented |
| 10 | Numerical consistency text ↔ data | PASS v1; **re-verified for v2** | Every number in v1 text traced to analysis.json; v2 text regenerated programmatically from analysis_v2.json |
| 11 | Traceability of every reported number | PASS | summary_by_condition.csv (v1) / summary_v2.csv (v2) + per-seed JSONL |
| 12 | OOD AUROC orientation correct | PASS | MSP with ID-as-positive; entropy fixed in v1 (bug documented, rerun, 24/24 exact) |

**v2 additions audit:** new analyses (TS, KMNIST, budgets, k=5, MNIST-ID) are *extensions* — labelled as such, each analyzed with the same machinery; Holm families defined per setting over the same five contrasts on raw NLL (mirroring the pre-registered primary) and separately on TS-NLL (labelled extension family).

---

## 4. Scope decisions (recorded for the revision log)

1. **Positioning chosen (of the three candidates):** **A+B hybrid — "budget-matched empirical comparison with mechanism evidence"**, honest about being a rigorous controlled empirical study, not a new algorithm. No algorithmic novelty is claimed.
2. **Architecture extension (CNN/CIFAR-10):** explicitly out of scope for this revision (CPU-bound); stated in Limitations with the paired-seed template offered for reuse. The paper does not claim generality beyond MLPs.
3. **SWA naming:** our "SWA" averages exactly the three cycle-end checkpoints (checkpoint-matched to Snapshot by design). The paper now states this is a *restricted* SWA schedule, distinguishes it from the standard many-checkpoint practice, and keeps the dense 40-checkpoint variant as the exploratory bridge.
4. **AUROC conventions:** MSP with in-distribution as positive class; both MSP and negative-entropy scores reported; KMNIST added as a second, harder probe.
