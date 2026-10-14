#!/usr/bin/env python3
"""v4.1 audit stage 3: SWA-dense, Table S1, secondary exceptions, budget sweep,
member stats, wall-clock/epoch claims, seed8 diagnosis cross-check, DE-SWA direct."""
import json, math
import numpy as np
from scipy import stats as st

R = '/home/z/my-project/v4-work/repo/results'
CHECKS = []
def check(loc, claim, value, ok):
    CHECKS.append((loc, claim, value, ok))
    print(f"[{'OK ' if ok else 'FAIL'}] {loc}: claimed {claim} | recomputed {value}")
def load(path): return [json.loads(l) for l in open(path)]
def perm_p(diffs):
    d = np.asarray(diffs, float); n = len(d); obs = abs(d.mean()); cnt = 0
    for mask in range(2 ** n):
        s = d.copy()
        for i in range(n):
            if (mask >> i) & 1: s[i] = -s[i]
        if abs(s.mean()) >= obs - 1e-12: cnt += 1
    return cnt / (2 ** n)
def t_ci(d):
    d = np.asarray(d, float); n = len(d); m = d.mean()
    se = d.std(ddof=1) / math.sqrt(n); tc = st.t.ppf(0.975, n - 1)
    return m, m - tc * se, m + tc * se
def close(a, b, tol=0.0005): return abs(a - b) <= tol

core = load(f'{R}/v2/experiment_v2_fmnist_B60_k3.jsonl')
B30 = load(f'{R}/v2/experiment_v2_fmnist_B30_k3.jsonl')
B120 = load(f'{R}/v2/experiment_v2_fmnist_B120_k3.jsonl')
k5 = load(f'{R}/v2/experiment_v2_fmnist_B60_k5.jsonl')
mnist = load(f'{R}/v2/experiment_v2_mnist_B60_k3.jsonl')
cf = load(f'{R}/cifar/experiment_cifar_B60_k3.jsonl')
v1 = load(f'{R}/experiment.jsonl')
sdense = load(f'{R}/experiment_swa_dense.jsonl')

print("=" * 100); print("SECTION G: DeepEns-SWA direct contrast (MNIST, replaces 'by adjacency')"); print("=" * 100)
d = np.array([r['deepens']['nll'] - r['swa']['nll'] for r in mnist])
m, lo, hi = t_ci(d); p = perm_p(d)
print(f"MNIST DE-SWA NLL: {m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f} (n=10)")
check('NEW S4.2', 'DE-SWA direct on MNIST (paper currently: by adjacency)', f'{m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f}', True)

# ECE mean ordering all settings
print(); print("-- ECE means by setting --")
for name, recs in [('core', core), ('B30', B30), ('B120', B120), ('k5', k5), ('mnist', mnist), ('cifar', cf)]:
    ems = {c: np.mean([r[c]['ece15'] for r in recs]) for c in ['single','deepens','snapshot','swa']}
    ordered = ems['deepens'] < ems['snapshot'] < ems['swa'] < ems['single']
    print(f"  {name:6s}: DE {ems['deepens']:.4f} SN {ems['snapshot']:.4f} SWA {ems['swa']:.4f} SG {ems['single']:.4f} strict={ordered}")
    check(f'ordering ECE {name}', 'DE<SN<SWA<SG', 'see above', ordered)
# NLL ordering all settings too
for name, recs in [('core', core), ('B30', B30), ('B120', B120), ('k5', k5), ('mnist', mnist), ('cifar', cf)]:
    ems = {c: np.mean([r[c]['nll'] for r in recs]) for c in ['single','deepens','snapshot','swa']}
    check(f'ordering NLL {name}', 'DE<SN<SWA<SG', f"DE {ems['deepens']:.4f} SN {ems['snapshot']:.4f} SWA {ems['swa']:.4f} SG {ems['single']:.4f}",
          ems['deepens'] < ems['snapshot'] < ems['swa'] < ems['single'])

print(); print("=" * 100); print("SECTION H: Table S1 (secondary contrasts, core, uncorrected P)"); print("=" * 100)
CONTRASTS = [('deepens','single'), ('snapshot','single'), ('swa','single'), ('deepens','snapshot'), ('snapshot','swa')]
tabS1 = {
 'acc': {('deepens','single'):(0.0070,0.0059,0.0082,0.0020), ('snapshot','single'):(0.0040,0.0025,0.0055,0.0020),
         ('swa','single'):(0.0031,0.0014,0.0048,0.0020), ('deepens','snapshot'):(0.0030,0.0019,0.0041,0.0039),
         ('snapshot','swa'):(0.0009,0.0004,0.0013,0.0078)},
 'brier': {('deepens','single'):(-0.0292,-0.0311,-0.0274,0.0020), ('snapshot','single'):(-0.0200,-0.0224,-0.0176,0.0020),
           ('swa','single'):(-0.0150,-0.0176,-0.0125,0.0020), ('deepens','snapshot'):(-0.0093,-0.0107,-0.0078,0.0020),
           ('snapshot','swa'):(-0.0050,-0.0053,-0.0046,0.0020)},
 'ece15': {('deepens','single'):(-0.0466,-0.0481,-0.0450,0.0020), ('snapshot','single'):(-0.0258,-0.0275,-0.0241,0.0020),
           ('swa','single'):(-0.0184,-0.0202,-0.0167,0.0020), ('deepens','snapshot'):(-0.0208,-0.0224,-0.0191,0.0020),
           ('snapshot','swa'):(-0.0073,-0.0080,-0.0067,0.0020)},
 'auroc_msp_mnist': {('deepens','single'):(0.0969,0.0847,0.1091,0.0020), ('snapshot','single'):(0.0423,0.0291,0.0555,0.0020),
           ('swa','single'):(-0.0029,-0.0166,0.0109,0.6406), ('deepens','snapshot'):(0.0546,0.0452,0.0640,0.0020),
           ('snapshot','swa'):(0.0452,0.0402,0.0501,0.0020)},
 'auroc_ent_mnist': {('deepens','single'):(0.1095,0.0970,0.1220,0.0020), ('snapshot','single'):(0.0497,0.0361,0.0633,0.0020),
           ('swa','single'):(0.0011,-0.0129,0.0152,0.8672), ('deepens','snapshot'):(0.0598,0.0499,0.0697,0.0020),
           ('snapshot','swa'):(0.0485,0.0434,0.0536,0.0020)},
}
for met, conds in tabS1.items():
    for c, (pd_, plo, phi, pp) in conds.items():
        d = np.array([r[c[0]][met] - r[c[1]][met] for r in core])
        m, lo, hi = t_ci(d); p = perm_p(d)
        check(f'TabS1 {met} {c[0]}-{c[1]}', f'{pd_:.4f} [{plo:.4f},{phi:.4f}] P={pp}',
              f'{m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f}',
              close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006) and abs(p - pp) < 0.0003)

print(); print("=" * 100); print("SECTION I: SWA-dense Table S2"); print("=" * 100)
seeds_swd = [r['seed'] for r in sdense]
by_seed = {r['seed']: r for r in sdense}
def swd(seed, met): return by_seed[seed][met]
def v1get(seed, cond, met):
    for r in v1:
        if r['seed'] == seed: return r[cond][met]
    raise KeyError(seed)
mets = {'nll': (0.3666, 0.0079), 'ece15': (0.0460, 0.0023), 'auroc_msp': (0.7458, 0.0149)}
for met, (pm, ps) in mets.items():
    v = np.array([swd(s, met) for s in seeds_swd], float)
    check(f'TabS2 swadense {met}', f'{pm}±{ps}', f'{v.mean():.4f}±{v.std(ddof=1):.4f}',
          close(v.mean(), pm) and close(v.std(ddof=1), ps, 0.0006))
tabS2c = {('nll','single'): (-0.1598,-0.1732,-0.1465), ('nll','snapshot'): (0.0182,0.0154,0.0209),
          ('ece15','single'): (-0.0242,-0.0260,-0.0224), ('ece15','snapshot'): (0.0016,0.0003,0.0029),
          ('auroc_msp','single'): (-0.0075,-0.0190,0.0041), ('auroc_msp','snapshot'): (-0.0498,-0.0561,-0.0435)}
for (met, cond), (pd_, plo, phi) in tabS2c.items():
    d = np.array([swd(s, met) - v1get(s, cond, met) for s in seeds_swd])
    m, lo, hi = t_ci(d)
    check(f'TabS2 {met} vs {cond}', f'{pd_:.4f} [{plo:.4f},{phi:.4f}]', f'{m:.4f} [{lo:.4f},{hi:.4f}]',
          close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006))

print(); print("=" * 100); print("SECTION J: secondary-metric exceptions (B30, k5) + budget sweep"); print("=" * 100)
# B30: acc Snapshot 0.8929 highest, DeepEns 0.8905 lowest, Single 0.8917
acc30 = {c: np.mean([r[c]['acc'] for r in B30]) for c in ['single','deepens','snapshot','swa']}
check('S4.2', 'B30 acc: Snapshot highest 0.8929', f"{acc30['snapshot']:.4f} (max={max(acc30, key=acc30.get)})", close(acc30['snapshot'], 0.8929, 0.0006) and max(acc30, key=acc30.get) == 'snapshot')
check('S4.2', 'B30 acc: DeepEns lowest 0.8905', f"{acc30['deepens']:.4f} (min={min(acc30, key=acc30.get)})", close(acc30['deepens'], 0.8905, 0.0006) and min(acc30, key=acc30.get) == 'deepens')
check('S4.2', 'B30 acc: Single 0.8917', f"{acc30['single']:.4f}", close(acc30['single'], 0.8917, 0.0006))
d = np.array([r['deepens']['acc'] - r['single']['acc'] for r in B30]); m, lo, hi = t_ci(d); p = perm_p(d)
check('S4.2', 'B30 DE-SG acc -0.0012 [-0.0021,-0.0002] P=0.018', f'{m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f}',
      close(m, -0.0012, 0.0006) and close(lo, -0.0021, 0.0006) and close(hi, -0.0002, 0.0006) and abs(p - 0.018) < 0.002)
b30_brier = {c: np.mean([r[c]['brier'] for r in B30]) for c in ['deepens','snapshot']}
check('S4.2', 'B30 Brier: Snapshot 0.1562 vs DeepEns 0.1573', f"SN {b30_brier['snapshot']:.4f} DE {b30_brier['deepens']:.4f}",
      close(b30_brier['snapshot'], 0.1562, 0.0006) and close(b30_brier['deepens'], 0.1573, 0.0006))
# k5: Snapshot acc 0.8944 vs DeepEns 0.8938
acc5 = {c: np.mean([r[c]['acc'] for r in k5]) for c in ['single','deepens','snapshot','swa']}
check('S4.2', 'k5 acc: Snapshot nominally highest 0.8944 vs DeepEns 0.8938',
      f"SN {acc5['snapshot']:.4f} DE {acc5['deepens']:.4f} max={max(acc5, key=acc5.get)}",
      close(acc5['snapshot'], 0.8944, 0.0006) and close(acc5['deepens'], 0.8938, 0.0006) and max(acc5, key=acc5.get) == 'snapshot')
# budget sweep Single NLL: 0.3795 -> 0.5265 -> 0.6672
for name, pv in [('B30', 0.3795), ('core', 0.5265), ('B120', 0.6672)]:
    recs = {'B30': B30, 'core': core, 'B120': B120}[name]
    v = np.mean([r['single']['nll'] for r in recs])
    check(f'S4.2 budget sweep {name}', f'Single NLL {pv}', f'{v:.4f}', close(v, pv))
# B30 Single ECE 0.049
e30 = np.mean([r['single']['ece15'] for r in B30])
check('S4.2', 'B30 Single ECE 0.049', f'{e30:.4f}', close(e30, 0.049, 0.0006))

# member stats: core member acc 0.8912 vs 0.8916; k5 member NLL 0.3212/0.3796; k5 JSD 0.0101/0.0107
de_ma = np.mean([r['deepens']['member_mean_acc'] for r in core])
sn_ma = np.mean([r['snapshot']['member_mean_acc'] for r in core])
print(f"core member acc: deepens {de_ma:.4f}, snapshot {sn_ma:.4f}")
check('S4.5', 'core member acc "0.8912 versus 0.8916"', f'DE {de_ma:.4f} SN {sn_ma:.4f}',
      (close(de_ma, 0.8912, 0.0006) and close(sn_ma, 0.8916, 0.0006)) or
      (close(de_ma, 0.8916, 0.0006) and close(sn_ma, 0.8912, 0.0006)))
de_mn5 = np.mean([r['deepens']['member_mean_nll'] for r in k5])
sn_mn5 = np.mean([r['snapshot']['member_mean_nll'] for r in k5])
check('S4.5', 'k5 member NLL 0.3212 versus 0.3796', f'DE {de_mn5:.4f} SN {sn_mn5:.4f}',
      close(de_mn5, 0.3212, 0.0006) and close(sn_mn5, 0.3796, 0.0006))
de_js5 = np.mean([r['deepens']['disagreement_jsd'] for r in k5])
sn_js5 = np.mean([r['snapshot']['disagreement_jsd'] for r in k5])
check('S4.5', 'k5 JSD 0.0101 versus 0.0107', f'DE {de_js5:.4f} SN {sn_js5:.4f}',
      close(de_js5, 0.0101, 0.0006) and close(sn_js5, 0.0107, 0.0006))

print(); print("=" * 100); print("SECTION K: wall-clock / epoch-count / reliability-diagram claims"); print("=" * 100)
wc = [r['wallclock_s'] for r in v1]
check('S3.3', 'B=60 MLP replicate 72-87 s wall-clock', f'{min(wc):.1f}-{max(wc):.1f} s',
      70 <= min(wc) and max(wc) <= 90)
ext_min = sum(r['wallclock_s'] for f in ['B30','B120','k5','mnist'] for r in load(f'{R}/v2/experiment_v2_{"fmnist_B30_k3" if f=="B30" else "fmnist_B120_k3" if f=="B120" else "fmnist_B60_k5" if f=="k5" else "mnist_B60_k3"}.jsonl'))
ext_min += sum(r['wallclock_s'] for r in core)
check('S3.3', 'extension settings ~69 minutes', f'{ext_min/60:.1f} min', 60 <= ext_min/60 <= 78)
cf_min = sum(r['wallclock_s'] for r in cf)
check('S3.3', 'CIFAR ~3.5 hours', f'{cf_min/3600:.2f} h', 3.0 <= cf_min/3600 <= 4.0)
# epoch accounting: core 1600 + extensions 8880 + cifar 1600 + swadense? -> ~12,800
# swa-dense: check run script wallclock & epochs
swd_wc = sum(r['wallclock_s'] for r in sdense)
print(f'   swa-dense total wallclock: {swd_wc/60:.1f} min (epochs not recorded in jsonl; run script needed)')
total_known = 1600 + 8880 + 1600
print(f'   known epochs: core 1600 + ext 8880 + cifar 1600 = {total_known}; paper claims ~12,800 total (implies ~{12800-total_known} for dense-SWA/pilots)')

# reliability diagram claim: single mean predicted confidence ~0.96 vs mean accuracy ~0.89
confs, accs = [], []
for r in core:
    rel = r['single']['reliability15']
    w = np.array(rel['bin_count'], float)
    c = np.array([x if x is not None else 0 for x in rel['bin_conf']], float)
    a = np.array([x if x is not None else 0 for x in rel['bin_acc']], float)
    confs.append((c * w).sum() / w.sum())
    accs.append((a * w).sum() / w.sum())
mc_, ma_ = np.mean(confs), np.mean(accs)
check('S4.1', 'single: typical predicted confidence ~0.96 matched by ~0.89 empirical',
      f'mean conf {mc_:.4f} vs mean acc {ma_:.4f}', 0.95 <= mc_ <= 0.97 and 0.88 <= ma_ <= 0.90)
# ECE reduction 66%
red = 1 - 0.0236/0.0702
check('S4.1', 'DeepEns 66% ECE reduction', f'{red*100:.1f}%', 63 <= red*100 <= 69)
# snapshot removed about a third, swa about a quarter
sn_red = (0.0702 - 0.0444)/0.0702; swa_red = (0.0702 - 0.0517)/0.0702
check('S4.1', 'Snapshot removed ~1/3 ECE, SWA ~1/4', f'SN {sn_red*100:.0f}% SWA {swa_red*100:.0f}%',
      28 <= sn_red*100 <= 39 and 21 <= swa_red*100 <= 31)

print(); print("=" * 100); print("SECTION L: seed-8 diagnosis cross-check + '20 fresh restarts' claim"); print("=" * 100)
diag = json.load(open(f'{R}/v4/seed8_diagnosis.json'))
print('   diagnosis keys:', list(diag.keys())[:10] if isinstance(diag, dict) else type(diag))
# member acc means: report C says other-nine member acc 0.7257; recompute
others = [r['deepens']['member_mean_acc'] for i, r in enumerate(cf) if i != 8]
om, osd = np.mean(others), np.std(others, ddof=1)
print(f'   other-nine member acc: {om:.4f}±{osd:.4f} (report C claims 0.7257±0.0042)')
check('report C (doc only)', 'other-nine member acc 0.7257±0.0042', f'{om:.4f}±{osd:.4f}',
      close(om, 0.7257, 0.0010))
# implied collapsed member acc
shared_acc = diag.get('members', {}).get('1', {}).get('test_acc') if isinstance(diag.get('members'), dict) else None
print('   diagnosis members info available:', shared_acc)

print()
print(f"=== STAGE 3: {len(CHECKS)} checks, {sum(1 for c in CHECKS if not c[3])} failures ===")
with open('/home/z/my-project/v4-work/verify_stage3.json', 'w') as f:
    json.dump({'n_checks': len(CHECKS), 'n_fail': sum(1 for c in CHECKS if not c[3]),
               'checks': [[str(x) for x in c] for c in CHECKS]}, f, indent=1)
