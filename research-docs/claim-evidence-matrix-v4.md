# Claim–Evidence Matrix v4 (drives the v3 → v4 revision)

**Manuscript:** "Deep ensembles outperform snapshot ensembles and weight
averaging for calibrated uncertainty under fixed training budgets" (v3 → v4)
**Date:** 13 October 2026 · **Evidence base:** raw per-seed JSONL (6 settings
× 10 seeds), independent recomputation (scripts/reanalysis_v4.py), seed-8
diagnostic re-run (scripts/diagnose_seed8.py).

Verification status legend: SUPPORTED (keep) · SCOPED (keep with narrower
domain) · REWORDED (claim changed) · FIXED-ERROR (v3 statement contradicted
the data).

---

## 1. Claims that the v3 manuscript makes, with verdicts

| ID | v3 claim (location) | Evidence after independent recomputation | Verdict | v4 action |
|----|---------------------|------------------------------------------|---------|-----------|
| C-01 | Abstract/§4.1: every strategy improves NLL over Single at matched budget; ordering DeepEns > Snapshot > SWA > Single on NLL (all Holm P=0.0098) | All 5 contrasts × 6 settings reproduce exactly from raw JSONL; all Holm P at the 0.0098 floor (all seeds agree in direction) | SUPPORTED | Keep; floor note already in §3.5 |
| C-02 | Abstract/§4.2: NLL/ECE ordering robust across budgets, k, direction, CIFAR replication | NLL ordering holds in all 6 settings. ECE mean ordering holds everywhere; the DeepEns−Snapshot ECE contrast is significant in all five digit settings (P=0.0020) but NOT on CIFAR (−0.0418, CI [−0.0845,+0.0008], P=0.082, inflated by the collapsed replicate 8) | SCOPED | Abstract keeps NLL-anchored claim; §4.6 reports the CIFAR ECE contrast explicitly with CI/P; contributions bullet re-worded |
| C-03 | Abstract/Intro/§4.4/Conclusion: "Only prediction averaging improved OOD detection …; SWA showed no improvement surviving multiple-comparison correction" | **Contradicted.** Under the within-probe 5-contrast Holm family (the same family structure as the pre-specified NLL families), SWA−Single is significantly POSITIVE on 6/11 setting×probe combinations (core KMNIST +0.0112 P_H=0.0234; B=30 both probes P_H=0.0098; k=5 KMNIST +0.0165 P_H=0.0117; CIFAR-100 +0.0247 P_H=0.0098), significantly NEGATIVE on 1/11 (B=120 MNIST probe −0.0157, P_H=0.0117), null on 4/11. DeepEns: significant on 11/11 (Δ +0.014…+0.121); Snapshot: 9/11 (null in the MNIST direction). Under a global 55-test family nothing survives (floor 0.0020×55=0.11), including DeepEns — so family-stable conclusions must be stated in terms of effect size and consistency, not a single global threshold | **FIXED-ERROR** | Rewritten in all five locations (Abstract, contribution bullet, §4.4, Discussion, Conclusion) to the comparative, heterogeneity-reporting form |
| C-04 | §4.3: "TS changed OOD AUROC by at most +0.012 on any condition or probe" | True only for the five MLP settings (max +0.0119). CIFAR: Single +0.0260, SWA +0.0186, Snapshot +0.0165, DeepEns +0.0035 | **FIXED-ERROR** (scope omitted CIFAR) | Scoped to MLP settings; CIFAR shifts reported; between-strategy OOD gaps on CIFAR compress (DeepEns−Single +0.069 → +0.046) without reversing |
| C-05 | Discussion: "Under shift, temperature scaling bought nothing—it changes confidence levels, not their ranking across inputs" | Theoretical claim is false in general: softmax(z/T) is not a rank-preserving transform of the maximum softmax across samples (it depends on the whole logit vector; for ensembles z = log p̄ mixes members). Empirically: shifts ≤ +0.012 (digit) and up to +0.026 (CIFAR) | **FIXED-ERROR** | Rewritten: TS can and did alter the ranking-based scores; effects small on digits, larger on CIFAR |
| C-06 | Discussion/practitioner guidance: "apply temperature scaling … does no harm to shift detection" | In all measured settings TS shifted OOD AUROC between −0.000 and +0.026 (never negative in the means) — no harm observed, but a guarantee is not supported | SCOPED | Conditional advice: check in the target setting |
| C-07 | §4.6: "the pattern extended to every in-distribution metric, including accuracy … and ECE" | True for means; the DeepEns−Snapshot ECE contrast on CIFAR is not significant (P=0.082); DeepEns−Single ECE significant everywhere (P=0.0020) | SCOPED | Contrast reported with CI and P; mean-vs-evidence distinction made explicit |
| C-08 | §4.6: "One of the ten replicates reversed the DeepEns–Snapshot ordering at seed level" | True (replicate 8: DeepEns NLL 0.929 vs Snapshot 0.882). Diagnostic re-run establishes the cause: the second fresh restart (seed 10812) collapsed to near-uniform predictions within the first epoch (train loss ≈ ln 10 ≈ 2.303 from epoch 1; logits → 0; val acc ≈ 0.10) and never recovered — a dead-network collapse under SGD lr 0.1 without normalisation layers. The other 29 fresh members across replicates trained normally; data, schedule and code verified; shared member reproduces bit-identically | SUPPORTED + now EXPLAINED | New paragraph in §4.6: diagnosis, retention decision (all seeds kept; no outcome-based exclusion), leave-one-out sensitivity (drop-8: DeepEns−Snapshot ECE −0.0607, P=0.0039; NLL −0.2075, P=0.0039; SWA OOD +0.0250, P=0.0039) |
| C-09 | §3.5: OOD contrasts "reported uncorrected throughout—five contrasts per probe" | Consistent with the pre-specified analysis (NLL/TS-NLL families only), but v3 never defined any corrected OOD analysis while simultaneously claiming (wrongly, C-03) that SWA's effects do not survive correction | UPGRADED | §3.5 + §4.4 add a labelled post-hoc robustness analysis: Holm within each setting×probe×score family (mirroring the primary family structure), setting-level and global sensitivities; all three reported for every strategy, not only SWA; explicitly marked post-hoc and defined after the CIFAR results were known |
| C-10 | §4.4: "DeepEns … the only strategy whose improvement over Single was significant on every combination" | True within-probe family: DeepEns 11/11; Snapshot 9/11; SWA 6/11 | SUPPORTED | Keep (with family definition now explicit) |
| C-11 | §4.4 core-setting SWA numbers (−0.0029 P=0.64; +0.0112 P=0.023 uncorrected) | Reproduce exactly | SUPPORTED | Keep; add corrected value (P_H=0.0234) |
| C-12 | Mechanism (member calibration + diversity; function- vs parameter-space averaging) | Member NLL/acc/JSD measurements reproduce; associational wording already present | SUPPORTED | Keep; add CIFAR nuance (weight average retained ~1/3 of the prediction-averaging OOD gain there), keeping the mechanism account explicitly associational |
| C-13 | Title "…under fixed training budgets" | Anchored on the primary outcome (NLL), with explicitly bounded secondary-metric exceptions | SUPPORTED | Keep; revision log documents rejected alternatives |
| C-14 | §4.4/abstract: MNIST-direction OOD P values labelled uncorrected | Fine | SUPPORTED | Keep |
| C-15 | README one-sentence summary: "only prediction averaging helps [OOD]" | Contradicted (same as C-03) | **FIXED-ERROR** | README updated |
| C-16 | §5 ready-answer/checklist: "OOD AUROC TS-invariant within ±0.012" | Contradicted for CIFAR | **FIXED-ERROR** | Checklist updated |

## 2. New analyses added in v4 (all from existing raw data; no new experiments)

1. **OOD multiplicity families (post-hoc, labelled):** within setting×probe×score
   5-contrast Holm; setting-level 10-contrast Holm; global 55-test sensitivity.
   Applied uniformly to DeepEns/Snapshot/SWA, MSP and entropy scores, all
   settings. New Supplementary Table S4.
2. **Previously unreported OOD results** (B=30, B=120, k=5 settings) added to
   Supplementary Table S4 — removing the selection in v3's OOD narrative
   (which reported only the core and MNIST-direction settings).
3. **TS-effect-on-OOD per condition** (digit + CIFAR) with the heterogeneity
   stated; the "ranking-invariance" sentence removed.
4. **CIFAR replicate-8 diagnosis** (deterministic re-run of the three members;
   per-epoch trajectories; per-member test metrics; reproduction gate on the
   shared member) and **leave-one-seed-out sensitivity** for all ten replicates
   on the key CIFAR contrasts.
5. **ECE contrasts with CIs and P values** for every setting (CIFAR
   DeepEns−Snapshot reported as not statistically resolved at n=10).

## 3. Family-choice sensitivity principle (stated in the paper)

The v4 text states explicitly: (i) the pre-specified multiplicity plan covers
NLL and TS-NLL only; (ii) the OOD family analyses are post-hoc robustness
analyses, defined after the CIFAR results were known; (iii) the qualitative
OOD conclusion rests on effect size and cross-setting consistency
(prediction averaging: larger, direction-consistent, significant on every
combination within the per-probe family; weight averaging: −0.016…+0.025,
mixed significance), which is stable across the family definitions tried;
(iv) no conclusion is drawn from a family chosen to make a specific contrast
significant or non-significant, and the global 55-test family (under which
nothing survives) is reported alongside the per-probe family.

## 4. Claims removed / weakened in v4

- "Only prediction averaging improved OOD detection" (all locations).
- "SWA showed no improvement surviving multiple-comparison correction" (all
  locations) — replaced by the heterogeneity-reporting form.
- "TS … changes confidence levels, not their ranking across inputs."
- "TS changed OOD AUROC by at most +0.012 on any condition or probe" (now
  scoped to the MLP settings, with CIFAR reported).
- "apply temperature scaling … does no harm to shift detection" (now
  conditional).
- "the cheapest-to-deploy single-trajectory variant (SWA) bought no shift
  robustness" (now "bought little and inconsistent shift robustness").
