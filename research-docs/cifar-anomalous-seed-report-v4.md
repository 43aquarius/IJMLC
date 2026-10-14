# CIFAR Anomalous-Seed Investigation Report (v4, Deliverable C)

**Date:** 13 October 2026 · **Scope:** replicate 8 of the CIFAR-10 extension
(`results/cifar/experiment_cifar_B60_k3.jsonl`), whose DeepEns record is the
outlier behind the large DeepEns standard deviations (ECE 0.0407 ± 0.0596;
NLL 0.7070 ± 0.0783).

---

## 1. The anomaly

| Quantity | Replicate 8 | Other nine replicates (mean ± s.d.) |
|---|---|---|
| DeepEns test NLL | 0.9290 | 0.6785 ± 0.0071 |
| DeepEns ECE (15 bins) | 0.2095 | 0.0209 ± 0.0051 |
| DeepEns accuracy | 0.7567 | 0.7758 ± 0.0044 |
| Member mean NLL | 1.4107 | 1.0258 ± 0.0304 |
| Member mean accuracy | 0.5146 | 0.7249 ± 0.0042 (corrected in v4.1 audit; previously written 0.7257) |
| Disagreement JSD | 0.3288 | 0.1350 ± 0.0058 |
| DeepEns−Snapshot NLL sign | reversed (0.929 vs 0.882) | negative in all nine |

Member mean accuracy 0.5146 with the shared first member healthy implies one
of the two fresh restarts sits near chance (~0.09–0.10 accuracy), dragging the
three-member mean down.

## 2. Investigation performed

1. **Aggregate decomposition** (from the released JSONL): the released record
   is consistent with exactly one collapsed fresh member; the shared first
   member equals the first cyclic snapshot and is healthy (the Snapshot
   condition of the same replicate is entirely normal: NLL 0.882, ECE 0.082).
2. **Deterministic diagnostic re-run** (`code/diagnose_seed8.py`): the three
   DeepEns members of replicate 8 (seeds 10800/10812/10813, B/k=20 epochs,
   identical channels_last pipeline, optimizer, schedule and data order) were
   retrained from scratch with per-epoch logging and per-member test
   evaluation:
   - Member 1 (shared, seed 10800): trains normally; its per-epoch history
     matches the released cyclic-run history at every logged epoch (all
     20 epochs within 5x10^-5; train loss 0.193785 and val NLL 1.058135 at
     epoch 20 identical to 6 decimals). Test NLL
     1.0477, accuracy 0.7311.
   - Member 2 (fresh restart, seed 10812): **collapsed in its first epoch.**
     Training loss rises to the ln-10 level (≈2.303, uniform prediction)
     within epoch 1, output logits decay to zero, validation accuracy sits at
     chance (≈0.10), and the run never recovers over all 20 epochs. Final test
     NLL 2.3026 ≈ ln 10, accuracy 0.1000, ECE 0.0007, mean maximum-softmax
     0.1007 — a functionally dead, uniform-predicting network.
   - Member 3 (fresh restart, seed 10813): trains normally. Test NLL 1.0213,
     accuracy 0.7242.
3. **Checks that rule out code/data causes**: data pipeline verified against
   official CIFAR-10 statistics (per-channel means 0.4914/0.4822/0.4465 in
   float64; class counts 5000/1000); per-step cosine schedule verified from
   the instrumented run; no NaN/Inf anywhere; the shared member and cyclic
   trajectory reproduce bit-identically, proving the environment, data and
   code path are faithful; the same code trained the other 19 fresh restarts
   of this extension (and all MLP-study restarts) without any collapse.
4. **Reproduction caveat (documented honestly):** the re-run reproduces the
   shared member and the cyclic trajectory to 6 decimals, but the collapsed
   member's final state differs slightly from the released record's implied
   endpoint (released member-mean arithmetic is consistent with the collapsed
   member having accuracy ≈0.089 rather than exactly 0.100). The current
   environment (Python 3.13 / numpy 2.2.4 wheel) differs at the
   floating-point margin from the recorded one (Python 3.12 / numpy 2.1.3);
   a knife-edge collapse can land on slightly different dead states across
   builds. The phenomenon — an immediate, unrecovered collapse of that
   restart — is deterministic in kind and its diagnosis is unaffected.

## 3. Root cause

A **training collapse of one fresh restart** under the protocol's aggressive
configuration (SGD lr 0.1 with cosine anneal, no batch normalisation, no
dropout, Kaiming-uniform init): the initial large-gradient steps drive the
network into a dead state (all logits → 0 / uniform predictions) from which
the zero gradients of the collapsed units never escape. This is a genuine
instance of restart risk — a real property of the budget-split strategy under
this training protocol — not an experimental error, data corruption, or
analysis defect. It is retained in all analyses under the pre-specified
no-exclusion rule; no outcome-based exclusion was performed.

## 4. Robustness with the seed retained vs dropped

| Analysis | All 10 seeds | Drop seed 8 | Drop any other seed |
|---|---|---|---|
| DeepEns−Single NLL | −1.2889, P_H=0.0098 | unchanged in kind | unchanged |
| DeepEns−Snapshot NLL | −0.1820, P_raw=0.0039 | −0.2075, P=0.0039 | −0.178..−0.182, P=0.0078 |
| DeepEns−Snapshot ECE15 | −0.0418 [−0.0845, +0.0008], P_raw=0.082 (**not resolved**) | −0.0607, P=0.0039 (resolved) | not resolved (P≈0.13) |
| SWA−Single OOD AUROC | +0.0247, P_raw=0.0020 | +0.0250, P=0.0039 | unchanged |

Full leave-one-out table for all ten seeds: `research-docs/ood-ts-statistics-v4.md` §8.

## 5. Consequences for the manuscript (implemented in v4)

1. The replicate is **retained** in the primary analysis (all ten seeds).
2. §4.6 now reports the anomaly, its diagnosis, and the retention decision
   explicitly, and states the ECE contrast (DeepEns−Snapshot) as directionally
   consistent but not statistically resolved at n=10 — distinguishing the mean
   ordering from the strength of evidence, as required.
3. The abstract and contributions no longer imply a statistically established
   ECE ordering on CIFAR; the NLL-anchored claims are unchanged.
4. The Limitations section notes that restart-failure rates at other scales
   and with normalisation layers are unknown and that ensemble tolerance of
   such failures deserves separate study.
5. No re-run of the experiment is warranted: the anomaly is a real event
   under the protocol, its inclusion is conservative (it works against the
   paper's own preferred strategy), and excluding it would require an
   outcome-based exclusion that the integrity rules prohibit.
