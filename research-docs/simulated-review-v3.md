# Simulated Peer Review (Deliverable H, v3 manuscript)

Three independent reviewer personas applied to the v3 manuscript
(12 October 2026). Each persona was given the full manuscript, the
supplementary material and access to the public repository. Reviews are
written as a real reviewer would write them, including disagreements.

---

## Reviewer A — Machine-learning methods researcher

**Overall evaluation.** This is a carefully controlled empirical study, not a
methodological innovation, and it is honest about that. The comparison design
is the contribution: budget-matched conditions with a shared first member and
checkpoint-matched Snapshot/SWA. The CIFAR-10 replication added in this
version addresses my main concern about the previous version (single
architecture family).

**Major strengths.**
1. The DeepEns–Snapshot and Snapshot–SWA contrasts are cleaner than anything
   in Ashukha et al. (2020) or Ovadia et al. (2019); the bit-identity
   verification of the shared member is unusual rigour.
2. The mechanism section connects member calibration and diversity to the
   outcome, with the correlational caveat stated.
3. The paper resists the temptation to rename standard methods; the
   contribution claim ("comparison design and measurement") is accurate.

**Major issues.**
1. *(Resolved this version)* Architecture generality — the CIFAR-10 CNN
   replication is convincing for the ordering, OOD separation and mechanism.
2. The SWA variant is a restricted 3-checkpoint average. The dense variant
   partially answers this, but a reviewer could still ask about
   cycle-frequency interactions (e.g., 6 shorter cycles at the same budget).
   This is a legitimate follow-up; the paper's limitation statement covers it.
3. The claim that temperature scaling leaves OOD AUROC "essentially unchanged"
   is supported within ±0.012 — fine, but the paper should (and now does) state
   this as a bounded observation rather than an invariance claim.

**Minor issues.** Fig. 1a's LR-schedule panel is display-only; consider
annotating checkpoint diamonds with epoch numbers. The term "budget-split"
is introduced without italics on first use.

**Needs additional experiments?** Not required for acceptance; the 6-cycle
SWA variant is a natural follow-up.

## Reviewer B — Experimental and statistical methodology researcher

**Overall evaluation.** The statistical reporting is well above the field's
median: seed-paired contrasts, exact permutation tests, Holm families,
pre-registration status explicitly separated from post-hoc extensions, and
all raw per-seed records released. I verified the arithmetic on a sample of
contrasts against the released JSONL and found no discrepancies.

**Major strengths.**
1. The v3 fixes the two over-claims I would otherwise have flagged: the
   every-metric ordering (now scoped to NLL/ECE with the B=30/k=5 exceptions
   quantified) and the B=30 post-TS reversal (now reported rather than
   glossed).
2. The clean-clone reproduction gate (fresh venv, fresh data, 110/110
   bit-identical values) is exemplary for this kind of paper.
3. The CIFAR extension's analysis plan was fixed before evaluation, and the
   paper labels the whole setting post-hoc. Correct.

**Major issues.**
1. With 10 seeds, the exact two-sided sign-flip test has a floor of 0.0020
   (uncorrected) / 0.0098 (Holm) — the paper reports this as "P=0.0098"
   repeatedly, which is the floor. A sentence noting that all significant
   core results sit at the test's resolution floor (i.e., every seed agrees
   in direction) would be more informative than the nominal value.
2. The OOD contrasts are secondary and uncorrected; the paper says so, but
   Table S1 reports many uncorrected P values, and the reader may count
   "significant" ones. A note on the family size per probe would help.
3. The MNIST-direction effect sizes are small (ΔNLL −0.016) even where
   significant; the practical-meaning discussion could quantify what a
   0.016-NLL difference buys. Not blocking.

**Needs additional experiments?** No. More seeds would be pleasant but the
permutation framework is already near its resolution floor at n=10 for the
effects in question.

## Reviewer C — Applied / deployment-oriented researcher

**Overall evaluation.** The question — how to spend a fixed training budget
for calibrated uncertainty — is the right practical question, and the answer
is clearly stated and honestly scoped. The new cost-accounting paragraph
(training vs wall-clock vs inference vs deployment) resolves my main
objection to the previous version, which read as if budget-matched training
meant matched deployment cost.

**Major strengths.**
1. The practitioner guidance is now actionable and conditional on an
   observable (is the long-trained baseline overconfident? — check a
   reliability diagram).
2. The inference-cost caveat (k forward passes for prediction averaging) is
   stated in Methods, Discussion and Limitations.
3. The OOD result has a clean practical reading: weight averaging, which is
   attractive precisely because it is free at inference, does not buy shift
   robustness.

**Major issues.**
1. The OOD probes are dataset-level shifts (MNIST/KMNIST vs Fashion-MNIST;
   CIFAR-100 vs CIFAR-10). No corruptions (CIFAR-10-C style) or covariate
   shifts — the practical situations most deployments face. The limitation
   is stated, but at least one corruption benchmark would materially
   strengthen the OOD section.
2. The models are small (34k–110k parameters) and the accuracies modest
   (71–90%). Whether the allocation rule transfers to the over-trained
   large-model regime, where overconfidence is well documented but so are
   diminishing returns from restarts, is genuinely open.
3. Wall-clock denomination: an epoch of a k-member ensemble costs the same as
   an epoch of a single model here, but practitioners may care about
   energy/latency; acknowledged in the paper.

**Needs additional experiments?** A CIFAR-10-C corruption suite would be my
one request, but it is an extension, not a gate.

---

## Synthesis and submission recommendation

**Agreement across reviewers.** The design's internal validity, the
statistical reporting, and the v3 honesty fixes (B=30 exceptions, TS reversal,
cost accounting, CIFAR replication) are strengths; no reviewer questions the
core findings' direction.

**Residual risks (ranked).**
1. Dataset-level OOD only (no corruptions/perturbations) — C's request; a
   follow-up experiment, not a validity threat to what is claimed.
2. Small models only — the paper's claims are explicitly bounded to this
   regime; risk is perceived narrowness, not over-claiming.
3. Restricted SWA schedule — covered by the dense-SWA control and the
   limitation statement.

**Changes that improve acceptance chances without new science:** the
floor-of-test sentence (B1), the family-size note for OOD (B2), and a
practical-magnitude gloss for small NLL differences (B3) — all cheap
additions I recommend making in the proofs stage.

**Recommendation.** The manuscript is at the level I would expect to see
sent to review at IJMLC, and I would support submission in its current
state. Predicting acceptance outcomes is not possible or attempted here.
