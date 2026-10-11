# Claim–Evidence Map (v2)

Every substantive claim in the v2 manuscript mapped to its evidence source. Claims with no
binding are not in the manuscript.

| # | Claim (location) | Evidence | Check |
|---|------------------|----------|-------|
| C1 | Every strategy improves NLL over Single at B=60/k=3 (Abstract; §4.1; Table 2) | results/analysis.json (v1, = v2 E-A) contrasts, Holm p=0.0098; identical values in v2 re-run | bit-verified |
| C2 | Strict ordering DeepEns > Snapshot > SWA > Single on all in-distribution metrics, core setting (§4.1) | analysis.json by_condition + contrasts (nll/acc/brier/ece15/ece10) | verified |
| C3 | Ordering robust across budgets 30/60/120 (§4.2; Fig 2a; Table 3) | analysis_v2.json fmnist_B{30,60,120}_k3 contrasts, all p_holm=0.0098 | verified |
| C4 | Budget-split advantage grows with budget: −0.075/−0.225/−0.332 (§4.2) | same contrasts, deepens_vs_single | verified |
| C5 | Single's NLL worsens with longer training (0.3795→0.5265→0.6672) while accuracy flat (§4.2) | by_condition nll/acc at 3 budgets | verified |
| C6 | Ordering robust at k=5; all strategies improve (§4.2; Fig 2b) | fmnist_B60_k5 contrasts | verified |
| C7 | MNIST direction: only DeepEns separates from Single (Δ=−0.0158 p=0.0098; Snapshot/SWA p=0.41) (§4.2; Fig 4a) | mnist_B60_k3 contrasts | verified |
| C8 | DeepEns beats Snapshot on MNIST (−0.0143, p=0.0098); Snapshot beats SWA (−0.0032, p=0.0098) (§4.2) | mnist_B60_k3 contrasts | verified |
| C9 | Fitted T mirrors overconfidence: 2.46/1.25/1.58/1.79 (§4.3; Fig 3b) | fmnist_B60_k3 by_condition ts.T | verified |
| C10 | TS leaves all five contrasts significant; DeepEns–Single after TS = −0.0434 [−0.0468,−0.0400] p=0.0098 (§4.3) | fmnist_B60_k3 ts.nll contrasts | verified |
| C11 | TS changes OOD AUROC by ≤ +0.012 and preserves between-strategy differences (§4.3) | ts.auroc_msp_* vs auroc_msp_* (max |Δ|=0.0113) | verified |
| C12 | TS: DeepEns remains significantly better than Single in every setting (§4.3; Table S3) | ts.nll contrasts all settings (−0.0434/−0.0114/−0.0567/−0.0384/−0.0071, p=0.0098) | verified |
| C13 | Low-budget TS-adjusted strategies within 0.014 NLL (§4.3, §5) | B30 ts.nll by_condition range 0.2986–0.3126 | verified |
| C14 | OOD core: DeepEns +0.0969 (MNIST probe); SWA −0.0029 p=0.64; KMNIST probe: DeepEns +0.1097 p=0.002; SWA +0.0112 p=0.023 (§4.4) | contrasts auroc_msp_mnist / auroc_msp_kmnist | verified |
| C15 | OOD generalises: DeepEns significant on all 4 probe–direction combos; single-trajectory n.s. on MNIST direction (§4.4; Fig 4b) | auroc_msp_{fmnist,kmnist} contrasts, mnist_B60_k3 (p=0.0078/0.0020) | verified |
| C16 | Mechanism: restart members better calibrated (0.3379 vs 0.4039) and more diverse (JSD 0.0150 vs 0.0106); same at k=5 (0.3212 vs 0.3796) (§4.5; Fig 1e,f) | member_mean_nll, disagreement_jsd in analysis files | verified |
| C17 | Dense SWA improves NLL but not OOD; still trails Snapshot (Suppl. S2/S3) | v1 experiment_swa_dense.jsonl + analysis | verified (v1) |
| C18 | Compute-exactness: 2B+(k−1)B/k epochs per replicate; shared first member bit-identical (§3.1) | run_experiments_v2.py; shared_member_bit_identical=true in all 5 settings (seed 0) | verified |
| C19 | v2 pipeline reproduces v1 bit-for-bit (§3.6) | 28/28 metrics seed-0 exact match | verified |
| C20 | Scope bounds (Abstract end; §5.1) | design description | n/a (statement of scope) |

**Overclaim audit:** the phrase "outperform" in the title is supported by: DeepEns significantly
beats Snapshot and (transitively, each pairwise significant) SWA on the primary outcome in
every one of the five settings; MNIST-direction boundary for Snapshot/SWA-vs-Single is stated
prominently (Abstract, §4.2, §5). No universality beyond the tested regime is claimed
anywhere; "calibrated uncertainty" in the title refers to the in-distribution metrics on which
the ordering is unanimous.
