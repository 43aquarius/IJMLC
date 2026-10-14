# Cover Letter — v4.1.1 submission draft

**To:** The Editor-in-Chief, International Journal of Machine Learning and Cybernetics
**From:** Chang Tan, Dalian University of Technology (corresponding author; aquars43@foxmail.com)
**Date:** 14 October 2026
**Manuscript:** *Deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty under fixed training budgets*
**Type:** Original research article

---

Dear Editor,

Please consider the enclosed manuscript for publication in the International Journal of Machine Learning and Cybernetics.

**Research question.** Method comparisons in uncertainty quantification typically train each method to its own best operating point, so the reported trade-offs vary budgets across methods. Practitioners face the inverse problem: a fixed compute allocation and a choice of how to spend it. The study asks which allocation of a fixed training budget buys the best-calibrated uncertainty, and which mechanism the difference is attributable to.

**Design.** Under an identical 60-epoch SGD budget (with budget, ensemble-size and architecture extensions), four allocation strategies are compared for a multilayer perceptron on Fashion-MNIST and, in a post-hoc replication, a small convolutional network on CIFAR-10: one long-trained network; a budget-split deep ensemble of three 20-epoch restarts; the cycle-end snapshot ensemble of one cyclic run; and the stochastic weight average of those snapshots. Two design features sharpen the comparisons: the snapshot ensemble and the weight average are derived from the *identical* checkpoints, so their contrast isolates the combination mechanism (prediction averaging versus weight averaging) free of run-to-run variation; and the first ensemble member is shared bit-identically between the two ensembles. All comparisons use seed-paired exact permutation inference with Holm correction over the pre-specified contrast family.

**Main empirical findings.** (i) Splitting the budget across independent restarts produced the best-calibrated uncertainty on the primary outcome (test negative log-likelihood) in every setting tested, with the four-way ordering preserved across budgets, ensemble sizes and a CIFAR-10 replication; on CIFAR-10, however, the deep-ensemble-versus-snapshot advantage in expected calibration error was directionally consistent but not statistically resolved at ten replicates. (ii) A boundary condition exists: on the near-saturated MNIST task, single-trajectory strategies showed no reliable improvement. (iii) In out-of-distribution detection, prediction averaging improved over the single network on every probe and direction, whereas weight averaging of the identical checkpoints showed small, task-dependent effects. (iv) Per-condition temperature scaling compressed but did not close the in-distribution gaps at the core budget and above.

**Nature of the contribution.** This is not a new-algorithm paper. The contribution is a compute-exact, checkpoint-matched controlled comparison with mechanism-level diagnostics and a bounded interpretation, released with complete per-replicate records, analysis code and figure source data. All conclusions are limited to the regimes actually measured (small networks, image tasks); anomalous replicates are retained and documented rather than excluded, and post-hoc analyses are labelled as such throughout.

I confirm that this manuscript is original, has not been published previously, and is not under consideration elsewhere. The author has no competing interests. A full data and code availability statement, an author-contribution statement, and a disclosure of large-language-model assistance in the research workflow appear in the manuscript's Statements and Declarations.

Thank you for your consideration.

Sincerely,

Chang Tan
Dalian University of Technology

---

*Notes for the author (not part of the letter): update the funding sentence, ORCID and submission-system fields per the final checklist before submission; verify the funding declaration matches your actual situation. The letter intentionally makes no claim of breakthrough novelty and does not reference acceptance likelihood.*
