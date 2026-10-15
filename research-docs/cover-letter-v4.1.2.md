# Cover Letter — v4.1.2 submission version

**To:** The Editor-in-Chief, International Journal of Machine Learning and Cybernetics
**From:** Chang Tan, Dalian University of Technology (sole and corresponding author; aquars43@foxmail.com)
**Date:** 15 October 2026
**Manuscript:** *Deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty under fixed training budgets*
**Type:** Original research article

> This markdown mirrors the submitted one-page letter
> (`cover-letter-Chang-Tan.docx` / `.pdf` in the submission package).

---

Dear Editor,

Please consider the manuscript referenced above for publication as an original research article.

**Research question.** Method comparisons in uncertainty quantification typically train each method to its own operating point; practitioners face the inverse problem of a fixed compute allocation and a choice of how to spend it. The study asks which allocation of a fixed training budget buys the best-calibrated uncertainty, and why.

**Design.** Under an identical 60-epoch SGD budget (with budget, ensemble-size and architecture extensions), four strategies are compared for a multilayer perceptron on Fashion-MNIST and, post-hoc, a small convolutional network on CIFAR-10: one long-trained network; a budget-split deep ensemble of three 20-epoch restarts; the snapshot ensemble of one cyclic run; and the stochastic weight average of those snapshots. The snapshot ensemble and the weight average derive from identical checkpoints, so their contrast isolates the combination mechanism, and the first ensemble member is shared bit-identically between the two ensembles. All comparisons use seed-paired exact permutation tests with Holm correction.

**Main empirical findings.** (i) Budget-split restarts produced the best-calibrated uncertainty on the primary outcome (test negative log-likelihood) in every setting tested, with the ordering preserved across budgets, ensemble sizes and the CIFAR-10 replication, where however the deep-ensemble-versus-snapshot advantage in expected calibration error was directionally consistent but not statistically resolved at ten replicates. (ii) On near-saturated MNIST, single-trajectory strategies showed no reliable improvement. (iii) In out-of-distribution detection, prediction averaging improved over the single network on every probe and direction, whereas weight averaging of the identical checkpoints showed small, task-dependent effects. (iv) Per-condition temperature scaling compressed but did not close the in-distribution gaps at the core budget and above.

**Nature of the contribution.** This is not a new-algorithm paper: the contribution is a compute-exact, checkpoint-matched controlled comparison with mechanism-level diagnostics, released with complete per-replicate records and analysis code. Conclusions are bounded to the regimes measured; anomalous replicates are retained, and post-hoc analyses are labelled as such.

**Fit to the journal.** The study concerns core machine-learning methodology (ensembles, prediction averaging and weight averaging) evaluated with the statistical rigour the journal's readership expects, and it addresses a practical question of broad interest: how to spend a fixed training budget for reliable, well-calibrated predictions.

**Declarations.** I confirm that the manuscript is original, has not been published previously, and is not under consideration elsewhere. I am the sole author; I have no competing interests, and no funding was received for this work. All code, raw per-replicate records and figure source data are publicly available at https://github.com/43aquarius/deep-ensembles-fixed-budget.

Thank you for your consideration.

Yours sincerely,

Chang Tan
Dalian University of Technology, Dalian, China
aquars43@foxmail.com
