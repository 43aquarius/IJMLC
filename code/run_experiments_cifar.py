#!/usr/bin/env python3
"""Cross-architecture extension: budget-matched four-way comparison on
CIFAR-10 with a small CNN (CIFAR-100 as the OOD probe).

Post-hoc extension (NOT pre-registered); see research-docs/experiment-plan-cifar.md.
Design mirrors run_experiments_v2.py exactly (seeds, schedules, metrics);
differences: model family (SmallCNN, channels_last), dataset, and
epoch-level checkpointing so that wall-clock-sharded execution is exactly
resumable (each shard continues mid-seed without altering training).

Per seed s, base = 10000 + 100*s:
  - Single        : B epochs, one cosine cycle, seed base+0
  - Cyclic run    : B epochs, K cosine cycles, seed base+0, snapshots at
                    B/K, 2B/K, ..., B
  - DeepEns-K     : {snapshot 1} + fresh runs seeds base+11..base+1K, B/K epochs
  - Snapshot-K    : the K cycle-end snapshots
  - SWA-K         : uniform weight average of the same K snapshots
  - seed 0 only   : fresh B/K-epoch run, seed base+0 (bit-identity check)

Usage:
  python run_experiments_cifar.py --budget 60 --k 3 --seeds 0:10 \
      --out results/cifar/experiment_cifar_B60_k3.jsonl [--time-budget 540]
Exit 42 = unfinished (resume by re-running the same command).
"""
import argparse
import json
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # shared metric implementations (bit-identical to v1/v2)
    nll, accuracy, brier, ece, ood_auroc, pairwise_jsd,
    fit_temperature, apply_temperature, log_probs_as_logits,
)
from common_cifar import (
    load_splits_cifar, TrainConfigCIFAR, train_run_cifar, SmallCNN,
    logits_of_cifar, probs_of_cifar, swa_state_dicts, lr_at_cifar,
)
import torch.nn.functional as F

torch.set_num_threads(int(os.environ.get("TORCH_THREADS", "2")))
import paths
CKPT_DIR = os.path.join(paths.RESULTS, "cifar", "ckpts")


def reliability(p, y, bins=15):
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


def train_piece(name, cfg, splits, ckpt_path, stop_after=None):
    """Train one piece with epoch-level checkpoint/resume (exact continuation).

    Identical computation to common_cifar.train_run_cifar: same model
    construction (seeded init), same optimizer, same data-order generator.
    Resume restores (epoch, model, optimizer, generator, snapshots).
    `stop_after` (debug/tests only) stops after that many epochs, leaving a
    resumable checkpoint.
    """
    if os.path.exists(ckpt_path):
        ck = torch.load(ckpt_path, weights_only=False)
        model = SmallCNN(0)
        model.load_state_dict(ck["model"])
        model = model.to(memory_format=torch.channels_last)
        opt = torch.optim.SGD(model.parameters(), lr=cfg.lr_max,
                              momentum=cfg.momentum, weight_decay=cfg.weight_decay)
        opt.load_state_dict(ck["opt"])
        g = torch.Generator()
        g.set_state(ck["gen"])
        epoch0, snapshots, history = ck["epoch"], ck["snapshots"], ck["history"]
    else:
        model = SmallCNN(cfg.seed)
        model = model.to(memory_format=torch.channels_last)
        opt = torch.optim.SGD(model.parameters(), lr=cfg.lr_max,
                              momentum=cfg.momentum, weight_decay=cfg.weight_decay)
        g = torch.Generator().manual_seed(cfg.seed + 1)
        epoch0, snapshots, history = 0, [], []

    X = torch.from_numpy(splits["train_x"]).to(memory_format=torch.channels_last)
    Y = torch.from_numpy(splits["train_y"])
    Xv = torch.from_numpy(splits["val_x"]).to(memory_format=torch.channels_last)
    Yv = torch.from_numpy(splits["val_y"])
    n = X.shape[0]
    spe = int(np.ceil(n / cfg.batch_size))

    for epoch in range(epoch0, cfg.epochs):
        model.train()
        perm = torch.randperm(n, generator=g)
        tl, seen = 0.0, 0
        for i in range(spe):
            bidx = perm[i * cfg.batch_size:(i + 1) * cfg.batch_size]
            step = epoch * spe + i
            lr = lr_at_cifar(step, cfg, spe)
            for grp in opt.param_groups:
                grp["lr"] = lr
            opt.zero_grad()
            out = model(X[bidx])
            loss = F.cross_entropy(out, Y[bidx])
            loss.backward()
            opt.step()
            tl += loss.item() * len(bidx)
            seen += len(bidx)
        model.eval()
        with torch.no_grad():
            vnll = F.cross_entropy(model(Xv), Yv).item()
        history.append(dict(epoch=epoch + 1, train_loss=tl / seen,
                             val_nll=vnll,
                             lr=lr_at_cifar((epoch + 1) * spe - 1, cfg, spe)))
        if cfg.snapshot and (epoch + 1) % (cfg.epochs // cfg.cycles) == 0:
            snapshots.append({k: v.detach().clone() for k, v in model.state_dict().items()})
        torch.save(dict(model=model.state_dict(), opt=opt.state_dict(),
                        gen=g.get_state(), epoch=epoch + 1,
                        snapshots=snapshots, history=history), ckpt_path)
        if stop_after is not None and (epoch + 1) >= stop_after:
            print(f"    [debug] stopping {name} after epoch {epoch+1}", flush=True)
            break
    model_sd = {k: v.detach().clone() for k, v in model.state_dict().items()}
    return model_sd, snapshots, history


def run_seed(s, splits, B, K, ckpt_dir):
    base = 10000 + 100 * s
    t0 = time.time()
    member_epochs = B // K

    pieces = {}
    specs = [
        ("single", TrainConfigCIFAR(epochs=B, cycles=1, seed=base + 0)),
        ("cyclic", TrainConfigCIFAR(epochs=B, cycles=K, seed=base + 0, snapshot=True)),
    ]
    for i in range(1, K):
        specs.append((f"m{i}", TrainConfigCIFAR(epochs=member_epochs, cycles=1,
                                                 seed=base + 10 + i)))
    if s == 0:
        specs.append(("check", TrainConfigCIFAR(epochs=member_epochs, cycles=1, seed=base + 0)))

    for name, cfg in specs:
        ck = os.path.join(ckpt_dir, f"s{s}_{name}.pt")
        pieces[name] = train_piece(name, cfg, splits, ck)
        print(f"    piece {name} done ({time.time()-t0:.0f}s elapsed)", flush=True)

    sd_single, _, hist_single = pieces["single"]
    sd_cyc, snaps, hist_cyc = pieces["cyclic"]
    assert len(snaps) == K
    member_sds = [snaps[0]] + [pieces[f"m{i}"][0] for i in range(1, K)]

    shared_check = None
    if s == 0:
        fresh_sd = pieces["check"][0]
        shared_check = all(torch.equal(fresh_sd[k], snaps[0][k]) for k in fresh_sd)
        print(f"    shared-member bit-identity: {shared_check}", flush=True)

    swa_sd = swa_state_dicts(snaps)

    Xtest, ytest = splits["test_x"], splits["test_y"]
    Xval, yval = splits["val_x"], splits["val_y"]
    oods = splits["oods"]

    res = dict(
        seed=s, base=base,
        config=dict(id="cifar10", budget=B, k=K, ood_probes=list(oods.keys())),
        versions=dict(torch=torch.__version__, numpy=np.__version__),
        shared_member_bit_identical=shared_check,
        histories=dict(single=hist_single, cyclic=hist_cyc),
    )

    def probs_on(sd, X):
        return probs_of_cifar(logits_of_cifar(sd, X))

    def eval_cond(p_test, p_val, ood_p_by_probe, members_p=None):
        r = dict(
            nll=nll(p_test, ytest), acc=accuracy(p_test, ytest),
            brier=brier(p_test, ytest),
            ece15=ece(p_test, ytest, 15), ece10=ece(p_test, ytest, 10),
        )
        for pname, p_ood in ood_p_by_probe.items():
            r[f"auroc_msp_{pname}"] = ood_auroc(p_test, p_ood, "msp")
            r[f"auroc_ent_{pname}"] = ood_auroc(p_test, p_ood, "entropy")
        r["reliability15"] = reliability(p_test, ytest, 15)
        z_val = log_probs_as_logits(p_val)
        T_hat, val_nll_ts = fit_temperature(z_val, yval)
        z_test = log_probs_as_logits(p_test)
        p_ts_test = apply_temperature(z_test, T_hat)
        ts = dict(T=T_hat, val_nll_ts=val_nll_ts)
        ts.update(dict(
            nll=nll(p_ts_test, ytest), acc=accuracy(p_ts_test, ytest),
            brier=brier(p_ts_test, ytest),
            ece15=ece(p_ts_test, ytest, 15), ece10=ece(p_ts_test, ytest, 10),
        ))
        for pname, p_ood in ood_p_by_probe.items():
            p_ts_ood = apply_temperature(log_probs_as_logits(p_ood), T_hat)
            ts[f"auroc_msp_{pname}"] = ood_auroc(p_ts_test, p_ts_ood, "msp")
            ts[f"auroc_ent_{pname}"] = ood_auroc(p_ts_test, p_ts_ood, "entropy")
        r["ts"] = ts
        if members_p is not None:
            r["member_mean_nll"] = float(np.mean([nll(p, ytest) for p in members_p]))
            r["member_mean_acc"] = float(np.mean([accuracy(p, ytest) for p in members_p]))
            r["disagreement_jsd"] = pairwise_jsd(members_p)
        return r

    def ens(l):  # ensemble mean probability
        return np.mean(np.stack(l, axis=0), axis=0)

    res["single"] = eval_cond(
        probs_on(sd_single, Xtest), probs_on(sd_single, Xval),
        {pn: probs_on(sd_single, od["x"]) for pn, od in oods.items()})
    dm_p_test = [probs_on(sd, Xtest) for sd in member_sds]
    dm_p_val = [probs_on(sd, Xval) for sd in member_sds]
    sn_p_test = [probs_on(sd, Xtest) for sd in snaps]
    sn_p_val = [probs_on(sd, Xval) for sd in snaps]
    res["deepens"] = eval_cond(
        ens(dm_p_test), ens(dm_p_val),
        {pn: ens([probs_on(sd, od["x"]) for sd in member_sds]) for pn, od in oods.items()},
        members_p=dm_p_test)
    res["snapshot"] = eval_cond(
        ens(sn_p_test), ens(sn_p_val),
        {pn: ens([probs_on(sd, od["x"]) for sd in snaps]) for pn, od in oods.items()},
        members_p=sn_p_test)
    res["swa"] = eval_cond(
        probs_on(swa_sd, Xtest), probs_on(swa_sd, Xval),
        {pn: probs_on(swa_sd, od["x"]) for pn, od in oods.items()})
    res["wallclock_s"] = time.time() - t0
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=60)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--seeds", default="0:10")
    ap.add_argument("--out", required=True)
    ap.add_argument("--time-budget", type=float, default=None,
                    help="seconds; stop before starting a new EPOCH-CHUNK "
                         "piece once exceeded (resumable). Exit 42 = unfinished.")
    args = ap.parse_args()

    a, b = (int(x) for x in args.seeds.split(":"))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    os.makedirs(CKPT_DIR, exist_ok=True)
    splits = load_splits_cifar()

    done = set()
    try:
        with open(args.out) as f:
            for line in f:
                done.add(json.loads(line)["seed"])
    except FileNotFoundError:
        pass

    t_start = time.time()
    all_done = True
    for s in range(a, b):
        if s in done:
            print(f"seed {s}: already done, skipping", flush=True)
            continue
        if args.time_budget is not None and time.time() - t_start > args.time_budget:
            print(f"time budget reached before seed {s}; stopping (resumable)",
                  flush=True)
            all_done = False
            break
        print(f"=== cifar10 B={args.budget} k={args.k} seed {s} ===", flush=True)
        r = run_seed(s, splits, args.budget, args.k, CKPT_DIR)
        with open(args.out, "a") as f:
            f.write(json.dumps(r) + "\n")
        # clean this seed's checkpoints
        for name in ["single", "cyclic"] + [f"m{i}" for i in range(1, args.k)] + ["check"]:
            p = os.path.join(CKPT_DIR, f"s{s}_{name}.pt")
            if os.path.exists(p):
                os.remove(p)
        print(f"seed {s} done in {r['wallclock_s']:.0f}s | "
              f"single NLL={r['single']['nll']:.4f} (TS {r['single']['ts']['nll']:.4f}) | "
              f"deepens NLL={r['deepens']['nll']:.4f} (TS {r['deepens']['ts']['nll']:.4f}) | "
              f"snapshot NLL={r['snapshot']['nll']:.4f} | "
              f"swa NLL={r['swa']['nll']:.4f} | "
              f"shared_ok={r['shared_member_bit_identical']}", flush=True)
    raise SystemExit(0 if all_done else 42)


if __name__ == "__main__":
    main()
