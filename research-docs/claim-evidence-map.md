# Writing base: claim–evidence map, terminology ledger, boundaries

## 论证脊柱 (one sentence)

In small-network image classification trained under a fixed SGD budget, this study finds that splitting the budget across three independently restarted, fully annealed runs (DeepEns) yields the most accurate and best-calibrated uncertainty—beating a cyclic-LR snapshot ensemble and both weight-averaging variants on NLL, calibration and OOD detection—supported by ten seeded, budget-matched, paired replications on Fashion-MNIST with an MNIST shift probe, and limited to this architecture scale, dataset family, budget and ensemble size.

## Evidence matrix

| ID | Claim | Evidence pointer | Type | Strength | Boundary | Action |
|---|---|---|---|---|---|---|
| C1 | All three strategies improve test NLL vs Single at matched budget | Table 2; Fig 1b | robust paired comparison, n=10, p_holm=0.0098 | strong | this regime only | keep |
| C2 | Ordering DeepEns > Snapshot > SWA on NLL/ECE/Brier | Table 1; Table 2 contrasts 4–5; Fig 1b | robust paired | strong | same | keep |
| C3 | Single long-trained model overconfident (ECE 0.070); DeepEns nearly calibrated (0.024) | Fig 1c; Suppl Fig 1; Table 1 | descriptive + robust contrast | strong | 15-bin ECE; 10-bin sensitivity agrees | keep |
| C4 | DeepEns improves OOD AUROC (+0.097), Snapshot partially (+0.042), SWA no evidence of improvement (Δ −0.003, CI crosses 0, p=0.64) | Fig 1d; Table 2 | robust paired (MSP score); entropy score agrees in direction for 4/5, SWA AUROC-ent +0.001 also ≈0 | strong for DeepEns/Snapshot; null-claim for SWA phrased as "no evidence" | single OOD pair (MNIST probe) | keep, calibrated wording |
| C5 | Mechanism (associational): DeepEns members individually better calibrated (member NLL 0.338 vs 0.404) and more diverse (JSD 0.0150 vs 0.0106) | Fig 1e,f; source data | descriptive | medium — association, not mediation proof | n=10 seeds, k=3 members | keep as explanation, explicitly associational |
| C6 | Prediction-averaging beats weight-averaging of the SAME 3 checkpoints (ΔNLL −0.038; ΔAUROC +0.045) | Table 2 contrast 5; Fig 1b,d | deterministic contrast (same trajectory), consistent across 10 seeds | strong | 3-checkpoint SWA variant | keep |
| C7 | Dense SWA (40 checkpoints) improves in-distribution NLL vs Single (−0.160) but still trails Snapshot (+0.018) and shows no OOD gain (−0.008, CI crosses 0) | Suppl Table S3; Suppl Fig 3 | exploratory (post hoc, uncorrected) | medium | labelled exploratory | keep, labelled |

## Terminology ledger

| Concept | Standard form | Notes |
|---|---|---|
| budget B | B = 60 epochs | identical for all conditions |
| ensemble size | k = 3 | fixed |
| conditions | Single; DeepEns; Snapshot; SWA; SWA-dense | capitalize as condition names |
| deep ensemble | budget-split independent restarts | cite Lakshminarayanan et al. |
| snapshot ensemble | cyclic-LR cycle-end checkpoints | cite Huang et al. |
| SWA-3 | uniform average of θ1, θ2, θ3 weights | matches Snapshot members exactly |
| SWA-dense | uniform average of epoch-end checkpoints 21–60 | exploratory |
| metrics | NLL; accuracy; Brier score; ECE (15 equal-width bins); AUROC (MSP / negative-entropy); JSD | JSD in nats |
| test set | Fashion-MNIST test (n=10,000) | touched once per condition per seed |
| OOD probe | MNIST test (n=10,000) | |

## Unresolved facts (AUTHOR_INPUT_NEEDED)

- Author names, affiliations, corresponding author, ORCID (cover currently attributes the workflow, not persons)
- Target journal choice and formatting pass
- Licence choice for code/data release

## Audience

Machine-learning researchers and practitioners who must allocate a fixed training budget; broad significance = every deployed classifier needs calibrated uncertainty, and the budget-matched question is what practitioners actually face.
