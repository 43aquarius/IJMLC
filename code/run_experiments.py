#!/usr/bin/env python3
"""Main experiment: budget-matched comparison of uncertainty strategies.

Per seed s (s = 0..9), base = 10000 + 100*s:
  - Single        : 60 epochs, one cosine cycle, seed base+0
  - Cyclic run    : 60 epochs, 3 cosine cycles, seed base+0, snapshots at 20/40/60
                    (snapshot 1 is bit-identical to a fresh 20-epoch run)
  - DeepEns-3     : {snapshot 1, fresh run seed base+10 (20 ep), fresh run seed base+11 (20 ep)}
  - Snapshot-3    : {snapshot 1, snapshot 2, snapshot 3}
  - SWA-3         : uniform weight average of the 3 snapshots
Test set and OOD probe are evaluated ONCE per condition per seed, after training.
Results are appended incrementally to results/experiment.jsonl (crash-safe).
"""
import json
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    TrainConfig, train_run, load_splits, logits_of, probs_of, ens_probs,
    evaluate_predictor, pairwise_jsd, swa_state_dicts, ece, accuracy, nll,
)

import paths
OUT = os.environ.get("BME_OUT", os.path.join(paths.RESULTS, "experiment.jsonl"))
N_SEEDS = 10
B = 60          # total budget in epochs
K = 3           # ensemble size
CHECK_SHARED = (B // K)  # epochs per member / per cycle


def hist_stats(p, bins=40):
    """Max-softmax histogram (for OOD score-distribution figure)."""
    conf = p.max(axis=1)
    h, edges = np.histogram(conf, bins=bins, range=(0.0, 1.0))
    return [int(v) for v in h], [float(e) for e in edges]


def reliability(p, y, bins=15):
    """Reliability diagram data (bin accuracy/confidence/counts)."""
    conf = p.max(axis=1)
    pred = p.argmax(axis=1)
    correct = (pred == y).astype(np.float64)
    edges = np.linspace(0.0, 1.0, bins + 1)
    idx = np.digitize(conf, edges[1:-1], right=False)
    acc, cnf, cnt = [], [], []
    for b in range(bins):
        m = idx == b
        acc.append(float(correct[m].mean()) if m.any() else None)
        cnf.append(float(conf[m].mean()) if m.any() else None)
        cnt.append(int(m.sum()))
    return dict(bin_acc=acc, bin_conf=cnf, bin_count=cnt)


def run_seed(s, sdata):
    base = 10000 + 100 * s
    t0 = time.time()

    # --- training (160 epochs total; 180 for seed 0 due to the bit-identity check)
    sd_single, _, hist_single = train_run(TrainConfig(epochs=B, cycles=1, seed=base + 0))
    sd_cyc, snaps, hist_cyc = train_run(
        TrainConfig(epochs=B, cycles=K, seed=base + 0, snapshot=True))
    assert len(snaps) == K

    member_sds = [snaps[0]]  # member 1 == snapshot 1 (verified for seed 0)
    for i in range(1, K):
        m_sd, _, m_hist = train_run(TrainConfig(epochs=CHECK_SHARED, cycles=1, seed=base + 10 + i))
        member_sds.append(m_sd)

    shared_check = None
    if s == 0:
        # implementation check: fresh 20-epoch run with same seed == snapshot 1
        fresh_sd, _, _ = train_run(TrainConfig(epochs=CHECK_SHARED, cycles=1, seed=base + 0))
        shared_check = all(
            torch.equal(fresh_sd[k], snaps[0][k]) for k in fresh_sd)

    swa_sd = swa_state_dicts(snaps)

    # --- evaluation (test set touched here, once per condition)
    res = dict(seed=s, base=base,
               versions=dict(torch=torch.__version__, numpy=np.__version__),
               shared_member_bit_identical=shared_check,
               histories=dict(single=hist_single, cyclic=hist_cyc))

    Xtest, Xood = sdata["test_x"], sdata["ood_x"]
    ytest = sdata["test_y"]

    def probs_list(states):
        return [probs_of(logits_of(sd, Xtest)) for sd in states]

    def cond_eval(name, p_test, p_ood, members_p=None):
        r = evaluate_predictor(p_test, sdata, p_ood)
        r["reliability15"] = reliability(p_test, ytest, 15)
        hin, _ = hist_stats(p_test)
        hout, _ = hist_stats(p_ood)
        r["msp_hist_in"] = hin
        r["msp_hist_out"] = hout
        if members_p is not None:
            r["member_mean_nll"] = float(np.mean([nll(p, ytest) for p in members_p]))
            r["member_mean_acc"] = float(np.mean([accuracy(p, ytest) for p in members_p]))
            r["disagreement_jsd"] = pairwise_jsd(members_p)
        res[name] = r

    # Single
    p_s = probs_of(logits_of(sd_single, Xtest))
    p_s_ood = probs_of(logits_of(sd_single, Xood))
    cond_eval("single", p_s, p_s_ood)

    # DeepEns-3
    dm_p = probs_list(member_sds)
    dm_ood = [probs_of(logits_of(sd, Xood)) for sd in member_sds]
    cond_eval("deepens", ens_probs(dm_p), ens_probs(dm_ood), members_p=dm_p)

    # Snapshot-3
    sn_p = probs_list(snaps)
    sn_ood = [probs_of(logits_of(sd, Xood)) for sd in snaps]
    cond_eval("snapshot", ens_probs(sn_p), ens_probs(sn_ood), members_p=sn_p)

    # SWA-3
    p_w = probs_of(logits_of(swa_sd, Xtest))
    p_w_ood = probs_of(logits_of(swa_sd, Xood))
    cond_eval("swa", p_w, p_w_ood)

    res["wallclock_s"] = time.time() - t0
    return res


def main():
    sdata = load_splits()
    done = set()
    try:
        with open(OUT) as f:
            for line in f:
                done.add(json.loads(line)["seed"])
    except FileNotFoundError:
        pass

    for s in range(N_SEEDS):
        if s in done:
            print(f"seed {s}: already done, skipping")
            continue
        print(f"=== seed {s} ===", flush=True)
        r = run_seed(s, sdata)
        with open(OUT, "a") as f:
            f.write(json.dumps(r) + "\n")
        key = r["single"]
        print(f"seed {s} done in {r['wallclock_s']:.0f}s | "
              f"single NLL={key['nll']:.4f} acc={key['acc']:.4f} | "
              f"deepens NLL={r['deepens']['nll']:.4f} | "
              f"snapshot NLL={r['snapshot']['nll']:.4f} | "
              f"swa NLL={r['swa']['nll']:.4f} | shared_ok={r['shared_member_bit_identical']}",
              flush=True)


if __name__ == "__main__":
    main()
