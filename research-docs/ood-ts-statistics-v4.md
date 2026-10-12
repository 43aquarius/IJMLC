# OOD and Temperature-Scaling Statistics Report (v4, Deliverable B)

**Date:** 13 October 2026 · **Source:** independent recomputation from raw
per-seed JSONL records (`code/reanalysis_v4.py`, output
`results/v4/reanalysis_v4.json`). Every number below is computed from
the released per-replicate records; the released `analysis_v2.json` and
`analysis_cifar.json` contrast statistics reproduce exactly.

## 1. Multiplicity families used in this report

| Family | Definition | Status |
|---|---|---|
| F1 | 5 contrasts on raw NLL, per setting | pre-specified (primary) |
| F2 | 5 contrasts on TS-NLL, per setting | secondary, pre-specified correction |
| Oa | 5 contrasts per setting x probe x score, Holm | **post-hoc** robustness (defined after CIFAR results known) |
| Ob | 10 contrasts per setting (both probes, MSP) | post-hoc sensitivity |
| Oc | all 55 MSP contrasts across all settings and probes | post-hoc global sensitivity |

With n=10 seeds the exact two-sided sign-flip floor is 2/1024 = 0.0019531
(written 0.0020); the Holm-adjusted floor within a 5-contrast family is
0.0098. A P at the floor means all ten seed-level deltas share one sign;
it is a statement about direction-unanimity at the test's resolution,
not an effect-size magnitude.

## 2. OOD detection (MSP AUROC): condition summaries

| Setting | Condition | AUROC mean | s.d. |
|---|---|---|---|
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | single | 0.6951 | 0.0116 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | deepens | 0.8048 | 0.0038 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | snapshot | 0.7536 | 0.0084 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | swa | 0.7063 | 0.0112 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | single | 0.7533 | 0.0172 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | deepens | 0.8502 | 0.0049 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | snapshot | 0.7956 | 0.0139 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | swa | 0.7504 | 0.0168 |
| Fashion-MNIST B=30 k=3 -> kmnist | single | 0.7113 | 0.0072 |
| Fashion-MNIST B=30 k=3 -> kmnist | deepens | 0.7912 | 0.0049 |
| Fashion-MNIST B=30 k=3 -> kmnist | snapshot | 0.7560 | 0.0069 |
| Fashion-MNIST B=30 k=3 -> kmnist | swa | 0.7216 | 0.0060 |
| Fashion-MNIST B=30 k=3 -> mnist | single | 0.7558 | 0.0129 |
| Fashion-MNIST B=30 k=3 -> mnist | deepens | 0.8532 | 0.0055 |
| Fashion-MNIST B=30 k=3 -> mnist | snapshot | 0.8077 | 0.0164 |
| Fashion-MNIST B=30 k=3 -> mnist | swa | 0.7734 | 0.0192 |
| Fashion-MNIST B=120 k=3 -> kmnist | single | 0.7017 | 0.0107 |
| Fashion-MNIST B=120 k=3 -> kmnist | deepens | 0.8222 | 0.0039 |
| Fashion-MNIST B=120 k=3 -> kmnist | snapshot | 0.7594 | 0.0062 |
| Fashion-MNIST B=120 k=3 -> kmnist | swa | 0.7075 | 0.0063 |
| Fashion-MNIST B=120 k=3 -> mnist | single | 0.7705 | 0.0226 |
| Fashion-MNIST B=120 k=3 -> mnist | deepens | 0.8552 | 0.0077 |
| Fashion-MNIST B=120 k=3 -> mnist | snapshot | 0.7993 | 0.0138 |
| Fashion-MNIST B=120 k=3 -> mnist | swa | 0.7548 | 0.0187 |
| Fashion-MNIST B=60 k=5 -> kmnist | single | 0.6951 | 0.0116 |
| Fashion-MNIST B=60 k=5 -> kmnist | deepens | 0.8073 | 0.0026 |
| Fashion-MNIST B=60 k=5 -> kmnist | snapshot | 0.7661 | 0.0098 |
| Fashion-MNIST B=60 k=5 -> kmnist | swa | 0.7116 | 0.0104 |
| Fashion-MNIST B=60 k=5 -> mnist | single | 0.7533 | 0.0172 |
| Fashion-MNIST B=60 k=5 -> mnist | deepens | 0.8617 | 0.0036 |
| Fashion-MNIST B=60 k=5 -> mnist | snapshot | 0.8150 | 0.0133 |
| Fashion-MNIST B=60 k=5 -> mnist | swa | 0.7586 | 0.0167 |
| MNIST B=60 k=3 (reversed direction) -> fmnist | single | 0.9264 | 0.0102 |
| MNIST B=60 k=3 (reversed direction) -> fmnist | deepens | 0.9403 | 0.0090 |
| MNIST B=60 k=3 (reversed direction) -> fmnist | snapshot | 0.9291 | 0.0089 |
| MNIST B=60 k=3 (reversed direction) -> fmnist | swa | 0.9276 | 0.0095 |
| MNIST B=60 k=3 (reversed direction) -> kmnist | single | 0.9165 | 0.0053 |
| MNIST B=60 k=3 (reversed direction) -> kmnist | deepens | 0.9399 | 0.0030 |
| MNIST B=60 k=3 (reversed direction) -> kmnist | snapshot | 0.9189 | 0.0048 |
| MNIST B=60 k=3 (reversed direction) -> kmnist | swa | 0.9141 | 0.0047 |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | single | 0.6799 | 0.0035 |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | deepens | 0.7488 | 0.0049 |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | snapshot | 0.7192 | 0.0034 |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | swa | 0.7046 | 0.0026 |

## 3. OOD contrasts versus Single (MSP): all settings and probes

Raw exact permutation P (primary reporting, pre-specified) and post-hoc
Holm-adjusted P within the setting-probe 5-contrast family (Oa).

| Setting | Probe | Contrast | mean delta | 95% CI | P_raw | P_Holm(Oa) |
|---|---|---|---|---|---|---|
| Fashion-MNIST B=60 k=3 (core, pre-registered) | kmnist | deepens - single | 0.1097 | [0.1004, 0.1190] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | kmnist | snapshot - single | 0.0585 | [0.0508, 0.0663] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | kmnist | swa - single | 0.0112 | [0.0023, 0.0202] | 0.0234 | 0.0234 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | kmnist | deepens - snapshot | 0.0511 | [0.0434, 0.0589] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | kmnist | snapshot - swa | 0.0473 | [0.0445, 0.0502] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | mnist | deepens - single | 0.0969 | [0.0847, 0.1091] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | mnist | snapshot - single | 0.0423 | [0.0291, 0.0555] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | mnist | swa - single | -0.0029 | [-0.0166, 0.0109] | 0.6406 | 0.6406 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | mnist | deepens - snapshot | 0.0546 | [0.0452, 0.0640] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | mnist | snapshot - swa | 0.0452 | [0.0402, 0.0501] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | kmnist | deepens - single | 0.0799 | [0.0730, 0.0868] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | kmnist | snapshot - single | 0.0447 | [0.0369, 0.0525] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | kmnist | swa - single | 0.0103 | [0.0039, 0.0167] | 0.0078 | 0.0098 |
| Fashion-MNIST B=30 k=3 | kmnist | deepens - snapshot | 0.0352 | [0.0305, 0.0398] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | kmnist | snapshot - swa | 0.0344 | [0.0324, 0.0364] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | mnist | deepens - single | 0.0974 | [0.0876, 0.1072] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | mnist | snapshot - single | 0.0520 | [0.0407, 0.0632] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | mnist | swa - single | 0.0176 | [0.0055, 0.0298] | 0.0078 | 0.0098 |
| Fashion-MNIST B=30 k=3 | mnist | deepens - snapshot | 0.0455 | [0.0355, 0.0555] | 0.0020 | 0.0098 |
| Fashion-MNIST B=30 k=3 | mnist | snapshot - swa | 0.0343 | [0.0316, 0.0370] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | kmnist | deepens - single | 0.1205 | [0.1117, 0.1293] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | kmnist | snapshot - single | 0.0577 | [0.0480, 0.0674] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | kmnist | swa - single | 0.0058 | [-0.0028, 0.0145] | 0.1621 | 0.1621 |
| Fashion-MNIST B=120 k=3 | kmnist | deepens - snapshot | 0.0628 | [0.0577, 0.0678] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | kmnist | snapshot - swa | 0.0519 | [0.0480, 0.0558] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | mnist | deepens - single | 0.0847 | [0.0724, 0.0970] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | mnist | snapshot - single | 0.0288 | [0.0189, 0.0387] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | mnist | swa - single | -0.0157 | [-0.0259, -0.0055] | 0.0117 | 0.0117 |
| Fashion-MNIST B=120 k=3 | mnist | deepens - snapshot | 0.0559 | [0.0503, 0.0615] | 0.0020 | 0.0098 |
| Fashion-MNIST B=120 k=3 | mnist | snapshot - swa | 0.0445 | [0.0396, 0.0494] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | kmnist | deepens - single | 0.1122 | [0.1026, 0.1218] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | kmnist | snapshot - single | 0.0710 | [0.0590, 0.0829] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | kmnist | swa - single | 0.0165 | [0.0050, 0.0280] | 0.0117 | 0.0117 |
| Fashion-MNIST B=60 k=5 | kmnist | deepens - snapshot | 0.0412 | [0.0342, 0.0482] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | kmnist | snapshot - swa | 0.0545 | [0.0522, 0.0567] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | mnist | deepens - single | 0.1084 | [0.0978, 0.1191] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | mnist | snapshot - single | 0.0617 | [0.0469, 0.0765] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | mnist | swa - single | 0.0053 | [-0.0099, 0.0205] | 0.4473 | 0.4473 |
| Fashion-MNIST B=60 k=5 | mnist | deepens - snapshot | 0.0467 | [0.0374, 0.0561] | 0.0020 | 0.0098 |
| Fashion-MNIST B=60 k=5 | mnist | snapshot - swa | 0.0564 | [0.0517, 0.0611] | 0.0020 | 0.0098 |
| MNIST B=60 k=3 (reversed direction) | fmnist | deepens - single | 0.0139 | [0.0057, 0.0221] | 0.0078 | 0.0312 |
| MNIST B=60 k=3 (reversed direction) | fmnist | snapshot - single | 0.0027 | [-0.0061, 0.0115] | 0.5039 | 1.0000 |
| MNIST B=60 k=3 (reversed direction) | fmnist | swa - single | 0.0011 | [-0.0085, 0.0108] | 0.7363 | 1.0000 |
| MNIST B=60 k=3 (reversed direction) | fmnist | deepens - snapshot | 0.0112 | [0.0037, 0.0188] | 0.0078 | 0.0312 |
| MNIST B=60 k=3 (reversed direction) | fmnist | snapshot - swa | 0.0016 | [0.0005, 0.0026] | 0.0039 | 0.0195 |
| MNIST B=60 k=3 (reversed direction) | kmnist | deepens - single | 0.0235 | [0.0191, 0.0278] | 0.0020 | 0.0098 |
| MNIST B=60 k=3 (reversed direction) | kmnist | snapshot - single | 0.0024 | [-0.0007, 0.0054] | 0.0898 | 0.1641 |
| MNIST B=60 k=3 (reversed direction) | kmnist | swa - single | -0.0024 | [-0.0051, 0.0003] | 0.0820 | 0.1641 |
| MNIST B=60 k=3 (reversed direction) | kmnist | deepens - snapshot | 0.0211 | [0.0184, 0.0238] | 0.0020 | 0.0098 |
| MNIST B=60 k=3 (reversed direction) | kmnist | snapshot - swa | 0.0048 | [0.0044, 0.0052] | 0.0020 | 0.0098 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | cifar100 | deepens - single | 0.0689 | [0.0635, 0.0743] | 0.0020 | 0.0098 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | cifar100 | snapshot - single | 0.0393 | [0.0366, 0.0420] | 0.0020 | 0.0098 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | cifar100 | swa - single | 0.0247 | [0.0224, 0.0269] | 0.0020 | 0.0098 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | cifar100 | deepens - snapshot | 0.0296 | [0.0249, 0.0343] | 0.0020 | 0.0098 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | cifar100 | snapshot - swa | 0.0146 | [0.0124, 0.0168] | 0.0020 | 0.0098 |

### Significance counts (Oa family, alpha = 0.05), versus Single

| Strategy | significant positive | significant negative | null | total |
|---|---|---|---|---|
| deepens | 11 | 0 | 0 | 11 |
| snapshot | 9 | 0 | 2 | 11 |
| swa | 5 | 1 | 5 | 11 |

## 4. OOD contrasts (negative-entropy score), versus Single

| Setting | Probe | mean delta | P_raw |
|---|---|---|---|
| Fashion-MNIST B=60 k=3 (core, pre-registered) | kmnist | SWA-Single 0.0134 | 0.0098 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | mnist | SWA-Single 0.0011 | 0.8672 |
| Fashion-MNIST B=30 k=3 | kmnist | SWA-Single 0.0143 | 0.0039 |
| Fashion-MNIST B=30 k=3 | mnist | SWA-Single 0.0248 | 0.0020 |
| Fashion-MNIST B=120 k=3 | kmnist | SWA-Single 0.0065 | 0.1328 |
| Fashion-MNIST B=120 k=3 | mnist | SWA-Single -0.0147 | 0.0137 |
| Fashion-MNIST B=60 k=5 | kmnist | SWA-Single 0.0197 | 0.0059 |
| Fashion-MNIST B=60 k=5 | mnist | SWA-Single 0.0112 | 0.1426 |
| MNIST B=60 k=3 (reversed direction) | fmnist | SWA-Single 0.0011 | 0.7461 |
| MNIST B=60 k=3 (reversed direction) | kmnist | SWA-Single -0.0025 | 0.0742 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | cifar100 | SWA-Single 0.0306 | 0.0020 |

(Full entropy tables for every contrast are in `results/v4/reanalysis_v4.json`;
SWA range across settings: -0.0147 to +0.0306.)

## 5. Global sensitivity (Oc family)

Family size: 55 MSP contrasts (6 settings x probes x 5 contrasts). Surviving Holm at 0.05: **none** (including every DeepEns contrast; the per-test floor 0.0020 x 55 = 0.109 > 0.05). This is why the manuscript's OOD conclusions rest on effect size and cross-setting consistency, and why the per-probe family (Oa), which mirrors the pre-specified NLL family structure, is the primary corrected view reported.

## 6. Temperature scaling: effect on OOD AUROC (delta = TS - raw, per condition)

| Setting | Condition | mean delta | per-seed range |
|---|---|---|---|
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | single | 0.0087 | [0.0050, 0.0110] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | deepens | 0.0064 | [0.0057, 0.0073] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | snapshot | 0.0110 | [0.0101, 0.0120] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> mnist | swa | 0.0113 | [0.0088, 0.0127] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | single | 0.0029 | [0.0013, 0.0042] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | deepens | 0.0036 | [0.0031, 0.0040] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | snapshot | 0.0055 | [0.0045, 0.0068] |
| Fashion-MNIST B=60 k=3 (core, pre-registered) -> kmnist | swa | 0.0053 | [0.0038, 0.0070] |
| Fashion-MNIST B=30 k=3 -> mnist | single | 0.0118 | [0.0090, 0.0143] |
| Fashion-MNIST B=30 k=3 -> mnist | deepens | 0.0034 | [0.0028, 0.0038] |
| Fashion-MNIST B=30 k=3 -> mnist | snapshot | 0.0088 | [0.0079, 0.0094] |
| Fashion-MNIST B=30 k=3 -> mnist | swa | 0.0099 | [0.0087, 0.0109] |
| Fashion-MNIST B=30 k=3 -> kmnist | single | 0.0057 | [0.0045, 0.0068] |
| Fashion-MNIST B=30 k=3 -> kmnist | deepens | 0.0020 | [0.0016, 0.0023] |
| Fashion-MNIST B=30 k=3 -> kmnist | snapshot | 0.0047 | [0.0039, 0.0053] |
| Fashion-MNIST B=30 k=3 -> kmnist | swa | 0.0053 | [0.0041, 0.0059] |
| Fashion-MNIST B=120 k=3 -> mnist | single | 0.0086 | [0.0036, 0.0136] |
| Fashion-MNIST B=120 k=3 -> mnist | deepens | 0.0078 | [0.0070, 0.0088] |
| Fashion-MNIST B=120 k=3 -> mnist | snapshot | 0.0096 | [0.0069, 0.0149] |
| Fashion-MNIST B=120 k=3 -> mnist | swa | 0.0107 | [0.0067, 0.0168] |
| Fashion-MNIST B=120 k=3 -> kmnist | single | -0.0000 | [-0.0020, 0.0036] |
| Fashion-MNIST B=120 k=3 -> kmnist | deepens | 0.0036 | [0.0027, 0.0043] |
| Fashion-MNIST B=120 k=3 -> kmnist | snapshot | 0.0035 | [0.0021, 0.0059] |
| Fashion-MNIST B=120 k=3 -> kmnist | swa | 0.0034 | [0.0017, 0.0065] |
| Fashion-MNIST B=60 k=5 -> mnist | single | 0.0087 | [0.0050, 0.0110] |
| Fashion-MNIST B=60 k=5 -> mnist | deepens | 0.0037 | [0.0032, 0.0040] |
| Fashion-MNIST B=60 k=5 -> mnist | snapshot | 0.0119 | [0.0102, 0.0132] |
| Fashion-MNIST B=60 k=5 -> mnist | swa | 0.0114 | [0.0094, 0.0147] |
| Fashion-MNIST B=60 k=5 -> kmnist | single | 0.0029 | [0.0013, 0.0042] |
| Fashion-MNIST B=60 k=5 -> kmnist | deepens | 0.0023 | [0.0021, 0.0025] |
| Fashion-MNIST B=60 k=5 -> kmnist | snapshot | 0.0060 | [0.0053, 0.0065] |
| Fashion-MNIST B=60 k=5 -> kmnist | swa | 0.0056 | [0.0046, 0.0063] |
| MNIST B=60 k=3 (reversed direction) -> fmnist | single | 0.0021 | [0.0009, 0.0034] |
| MNIST B=60 k=3 (reversed direction) -> fmnist | deepens | 0.0018 | [0.0015, 0.0022] |
| MNIST B=60 k=3 (reversed direction) -> fmnist | snapshot | 0.0024 | [0.0013, 0.0036] |
| MNIST B=60 k=3 (reversed direction) -> fmnist | swa | 0.0026 | [0.0014, 0.0039] |
| MNIST B=60 k=3 (reversed direction) -> kmnist | single | 0.0018 | [0.0011, 0.0024] |
| MNIST B=60 k=3 (reversed direction) -> kmnist | deepens | 0.0013 | [0.0012, 0.0016] |
| MNIST B=60 k=3 (reversed direction) -> kmnist | snapshot | 0.0019 | [0.0010, 0.0024] |
| MNIST B=60 k=3 (reversed direction) -> kmnist | swa | 0.0020 | [0.0009, 0.0025] |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | single | 0.0260 | [0.0241, 0.0280] |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | deepens | 0.0035 | [-0.0085, 0.0073] |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | snapshot | 0.0165 | [0.0148, 0.0191] |
| CIFAR-10 B=60 k=3 (post-hoc extension) -> cifar100 | swa | 0.0186 | [0.0172, 0.0205] |

Digit-task maximum |delta| = +0.0119; CIFAR-10 maximum = +0.0260 (Single). No condition-probe mean delta is negative.

## 7. ECE (15-bin) contrasts, all settings

| Setting | Contrast | mean delta | 95% CI | P_raw |
|---|---|---|---|---|
| Fashion-MNIST B=60 k=3 (core, pre-registered) | deepens - single | -0.0466 | [-0.0481, -0.0450] | 0.0020 |
| Fashion-MNIST B=60 k=3 (core, pre-registered) | deepens - snapshot | -0.0208 | [-0.0224, -0.0191] | 0.0020 |
| Fashion-MNIST B=30 k=3 | deepens - single | -0.0343 | [-0.0354, -0.0331] | 0.0020 |
| Fashion-MNIST B=30 k=3 | deepens - snapshot | -0.0122 | [-0.0134, -0.0109] | 0.0020 |
| Fashion-MNIST B=120 k=3 | deepens - single | -0.0466 | [-0.0484, -0.0447] | 0.0020 |
| Fashion-MNIST B=120 k=3 | deepens - snapshot | -0.0250 | [-0.0267, -0.0234] | 0.0020 |
| Fashion-MNIST B=60 k=5 | deepens - single | -0.0561 | [-0.0576, -0.0546] | 0.0020 |
| Fashion-MNIST B=60 k=5 | deepens - snapshot | -0.0230 | [-0.0250, -0.0209] | 0.0020 |
| MNIST B=60 k=3 (reversed direction) | deepens - single | -0.0051 | [-0.0057, -0.0044] | 0.0020 |
| MNIST B=60 k=3 (reversed direction) | deepens - snapshot | -0.0044 | [-0.0052, -0.0037] | 0.0020 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | deepens - single | -0.1805 | [-0.2234, -0.1376] | 0.0020 |
| CIFAR-10 B=60 k=3 (post-hoc extension) | deepens - snapshot | -0.0418 | [-0.0845, 0.0008] | 0.0820 |

## 8. CIFAR leave-one-seed-out sensitivity (exploratory)

| Dropped seed | DE-SN NLL | P | DE-SN ECE15 | P | SWA-SG AUROC | P |
|---|---|---|---|---|---|---|
| 0 | -0.1793 | 0.0078 | -0.0396 | 0.1328 | 0.0248 | 0.0039 |
| 1 | -0.1795 | 0.0078 | -0.0395 | 0.1328 | 0.0251 | 0.0039 |
| 2 | -0.1783 | 0.0078 | -0.0394 | 0.1328 | 0.0247 | 0.0039 |
| 3 | -0.1776 | 0.0078 | -0.0410 | 0.1289 | 0.0247 | 0.0039 |
| 4 | -0.1777 | 0.0078 | -0.0391 | 0.1484 | 0.0249 | 0.0039 |
| 5 | -0.1791 | 0.0078 | -0.0396 | 0.1328 | 0.0239 | 0.0039 |
| 6 | -0.1785 | 0.0078 | -0.0397 | 0.1328 | 0.0243 | 0.0039 |
| 7 | -0.1821 | 0.0078 | -0.0397 | 0.1289 | 0.0245 | 0.0039 |
| 8 | -0.2075 | 0.0039 | -0.0607 | 0.0039 | 0.0250 | 0.0039 |
| 9 | -0.1806 | 0.0078 | -0.0402 | 0.1289 | 0.0248 | 0.0039 |

With all ten seeds: DE-SN NLL -0.1820 (P_raw 0.0039), DE-SN ECE15 -0.0418
(P_raw 0.0820, not resolved), SWA-SG AUROC +0.0247 (P_raw 0.0020). Dropping
seed 8 (the replicate with the collapsed restart member) resolves the ECE
contrast; no other seed's removal does.
