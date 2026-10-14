#!/usr/bin/env python3
"""v4.1 audit stage 2: OOD (Table S4), ECE contrasts, CIFAR, SWA-dense, anomalous seed, wall-clock."""
import json, math
import numpy as np
from scipy import stats as st

R = '/home/z/my-project/v4-work/repo/results'
CHECKS = []
def check(loc, claim, value, ok):
    CHECKS.append((loc, claim, value, ok))
    print(f"[{'OK ' if ok else 'FAIL'}] {loc}: claimed {claim} | recomputed {value}")

def load(path):
    return [json.loads(l) for l in open(path)]

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

def holm(pvals):
    p = np.asarray(pvals, float); order = np.argsort(p); m = len(p)
    adj = np.empty(m); prev = 0.0
    for rank, idx in enumerate(order):
        a = min(1.0, (m - rank) * p[idx]); a = max(a, prev); adj[idx] = a; prev = a
    return adj

CONTRASTS = [('deepens','single'), ('snapshot','single'), ('swa','single'),
             ('deepens','snapshot'), ('snapshot','swa')]

def family(recs, val):
    """val: fn(r, cond) -> float. Returns dict contrast -> (m, lo, hi, p, holm)."""
    out = {}
    for c in CONTRASTS:
        a = np.array([val(r, c[0]) for r in recs], float)
        b = np.array([val(r, c[1]) for r in recs], float)
        d = a - b
        m, lo, hi = t_ci(d); p = perm_p(d)
        out[c] = (m, lo, hi, p)
    hs = holm([out[c][3] for c in CONTRASTS])
    for c, h in zip(CONTRASTS, hs):
        out[c] = out[c] + (h,)
    return out

files = {
    'core':  f'{R}/v2/experiment_v2_fmnist_B60_k3.jsonl',
    'B30':   f'{R}/v2/experiment_v2_fmnist_B30_k3.jsonl',
    'B120':  f'{R}/v2/experiment_v2_fmnist_B120_k3.jsonl',
    'k5':    f'{R}/v2/experiment_v2_fmnist_B60_k5.jsonl',
    'mnist': f'{R}/v2/experiment_v2_mnist_B60_k3.jsonl',
    'cifar': f'{R}/cifar/experiment_cifar_B60_k3.jsonl',
}
data = {k: load(v) for k, v in files.items()}
ssettings = {'core': 'Fashion-MNIST B60 k3 (core)', 'B30': 'B30', 'B120': 'B120',
             'k5': 'k5', 'mnist': 'MNIST B60 (reversed)', 'cifar': 'CIFAR-10'}

# ---------- Table S4: OOD MSP contrasts ----------
print("=" * 100); print("SECTION E: Table S4 OOD MSP contrasts (all 11 setting-probe combos)"); print("=" * 100)
tabS4 = {  # (setting, probe): {contrast: (delta, lo, hi, p_raw, p_holm)}
 ('core','kmnist'): {('deepens','single'):(0.1097,0.1004,0.1190,0.0020,0.0098),('snapshot','single'):(0.0585,0.0508,0.0663,0.0020,0.0098),('swa','single'):(0.0112,0.0023,0.0202,0.0234,0.0234)},
 ('core','mnist'): {('deepens','single'):(0.0969,0.0847,0.1091,0.0020,0.0098),('snapshot','single'):(0.0423,0.0291,0.0555,0.0020,0.0098),('swa','single'):(-0.0029,-0.0166,0.0109,0.6406,0.6406)},
 ('B30','kmnist'): {('deepens','single'):(0.0799,0.0730,0.0868,0.0020,0.0098),('snapshot','single'):(0.0447,0.0369,0.0525,0.0020,0.0098),('swa','single'):(0.0103,0.0039,0.0167,0.0078,0.0098)},
 ('B30','mnist'): {('deepens','single'):(0.0974,0.0876,0.1072,0.0020,0.0098),('snapshot','single'):(0.0520,0.0407,0.0632,0.0020,0.0098),('swa','single'):(0.0176,0.0055,0.0298,0.0078,0.0098)},
 ('B120','kmnist'): {('deepens','single'):(0.1205,0.1117,0.1293,0.0020,0.0098),('snapshot','single'):(0.0577,0.0480,0.0674,0.0020,0.0098),('swa','single'):(0.0058,-0.0028,0.0145,0.1621,0.1621)},
 ('B120','mnist'): {('deepens','single'):(0.0847,0.0724,0.0970,0.0020,0.0098),('snapshot','single'):(0.0288,0.0189,0.0387,0.0020,0.0098),('swa','single'):(-0.0157,-0.0259,-0.0055,0.0117,0.0117)},
 ('k5','kmnist'): {('deepens','single'):(0.1122,0.1026,0.1218,0.0020,0.0098),('snapshot','single'):(0.0710,0.0590,0.0829,0.0020,0.0098),('swa','single'):(0.0165,0.0050,0.0280,0.0117,0.0117)},
 ('k5','mnist'): {('deepens','single'):(0.1084,0.0978,0.1191,0.0020,0.0098),('snapshot','single'):(0.0617,0.0469,0.0765,0.0020,0.0098),('swa','single'):(0.0053,-0.0099,0.0205,0.4473,0.4473)},
 ('mnist','fmnist'): {('deepens','single'):(0.0139,0.0057,0.0221,0.0078,0.0312),('snapshot','single'):(0.0027,-0.0061,0.0115,0.5039,1.0000),('swa','single'):(0.0011,-0.0085,0.0108,0.7363,1.0000)},
 ('mnist','kmnist'): {('deepens','single'):(0.0235,0.0191,0.0278,0.0020,0.0098),('snapshot','single'):(0.0024,-0.0007,0.0054,0.0898,0.1641),('swa','single'):(-0.0024,-0.0051,0.0003,0.0820,0.1641)},
 ('cifar','cifar100'): {('deepens','single'):(0.0689,0.0635,0.0743,0.0020,0.0098),('snapshot','single'):(0.0393,0.0366,0.0420,0.0020,0.0098),('swa','single'):(0.0247,0.0224,0.0269,0.0020,0.0098)},
}
def close(a, b, tol=0.0005): return abs(a - b) <= tol

for (setting, probe), conds in tabS4.items():
    recs = data[setting]
    fam = family(recs, lambda r, c: r[c][f'auroc_msp_{probe}'])
    for c, (pd_, plo, phi, pp, ph) in conds.items():
        m, lo, hi, p, h = fam[c]
        ok = (close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006)
              and abs(p - pp) < 0.0003 and abs(h - ph) < 0.0003)
        check(f'TabS4 {setting}->{probe} {c[0]}-single',
              f'{pd_:.4f} [{plo:.4f},{phi:.4f}] P={pp} H={ph}',
              f'{m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f} H={h:.4f}', ok)

# text claims from S4.4
print(); print("-- S4.4 text claims --")
# SWA significance counts under Oa
swa_counts = {'pos': 0, 'neg': 0, 'null': 0}
de_sig = 0; sn_sig = 0
for (setting, probe) in tabS4:
    recs = data[setting]
    fam = family(recs, lambda r, c: r[c][f'auroc_msp_{probe}'])
    for c in [('deepens','single'), ('snapshot','single'), ('swa','single')]:
        m, lo, hi, p, h = fam[c]
        if c[0] == 'deepens' and h < 0.05: de_sig += 1
        if c[0] == 'snapshot' and h < 0.05: sn_sig += 1
        if c[0] == 'swa':
            if h < 0.05 and m > 0: swa_counts['pos'] += 1
            elif h < 0.05 and m < 0: swa_counts['neg'] += 1
            else: swa_counts['null'] += 1
check('S4.4', 'DeepEns significant on 11/11 Oa families', f'{de_sig}/11', de_sig == 11)
check('S4.4', 'Snapshot significant on 9/11', f'{sn_sig}/11', sn_sig == 9)
check('S4.4', 'SWA: 5 pos-sig, 1 neg-sig, 5 null', str(swa_counts),
      swa_counts == {'pos': 5, 'neg': 1, 'null': 5})

# SWA effect range -0.016 to +0.025 (text says effects ranged from -0.016 to +0.025)
swa_effects = []
for (setting, probe) in tabS4:
    recs = data[setting]
    d = np.mean([r['swa'][f'auroc_msp_{probe}'] - r['single'][f'auroc_msp_{probe}'] for r in recs])
    swa_effects.append(d)
check('S4.4', 'SWA-Single effect range -0.016..+0.025',
      f'{min(swa_effects):.4f}..{max(swa_effects):.4f}',
      close(min(swa_effects), -0.016, 0.0006) and close(max(swa_effects), 0.025, 0.0006))

# entropy-score SWA range -0.015 to +0.031
ent_effects = []
for setting, probes in [('core',['mnist','kmnist']),('B30',['mnist','kmnist']),('B120',['mnist','kmnist']),('k5',['mnist','kmnist']),('mnist',['fmnist','kmnist']),('cifar',['cifar100'])]:
    for probe in probes:
        d = np.mean([r['swa'][f'auroc_ent_{probe}'] - r['single'][f'auroc_ent_{probe}'] for r in data[setting]])
        ent_effects.append(d)
check('S4.4/abstract', 'entropy SWA range -0.015..+0.031', f'{min(ent_effects):.4f}..{max(ent_effects):.4f}',
      close(min(ent_effects), -0.015, 0.0006) and close(max(ent_effects), 0.031, 0.0006))

# core-setting text numbers: DE +0.0969 [+0.0847,+0.1091] P=0.0020; KMNIST +0.1097 [+0.1004,+0.1190]
# SWA core: -0.0029 [-0.0166,+0.0109] P=0.64; +0.0112 [+0.0023,+0.0202] P=0.023; Snapshot +0.0423/+0.0585  (verified in S4 table above)

# MNIST direction: DE +0.0139 P=0.008 and +0.0235 P=0.002 (uncorrected) -> verified in S4
# SWA interval width ~0.028 (MNIST probe core): (-0.0166..0.0109) width = 0.0275
w = 0.0109 - (-0.0166)
check('S4.4', 'SWA core MNIST-probe CI width about 0.028', f'{w:.4f}', close(w, 0.028, 0.0006))

# ---------- ECE contrasts (ood-ts stats section 7 + paper text) ----------
print(); print("-- ECE contrasts --")
ece_claims = {
 ('core','deepens','single'): (-0.0466, -0.0481, -0.0450, 0.0020),
 ('core','deepens','snapshot'): (-0.0208, -0.0224, -0.0191, 0.0020),
 ('mnist','deepens','single'): (-0.0051, -0.0057, -0.0044, 0.0020),
 ('mnist','deepens','snapshot'): (-0.0044, -0.0052, -0.0037, 0.0020),
 ('cifar','deepens','single'): (-0.1805, -0.2234, -0.1376, 0.0020),
 ('cifar','deepens','snapshot'): (-0.0418, -0.0845, 0.0008, 0.0820),
}
for (setting, a, b), (pd_, plo, phi, pp) in ece_claims.items():
    recs = data[setting]
    d = np.array([r[a]['ece15'] - r[b]['ece15'] for r in recs])
    m, lo, hi = t_ci(d); p = perm_p(d)
    check(f'ECE {setting} {a}-{b}', f'{pd_:.4f} [{plo:.4f},{phi:.4f}] P={pp}',
          f'{m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f}',
          close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006) and abs(p - pp) < 0.0003)

# ---------- CIFAR section (tab:cifar + text) ----------
print(); print("=" * 100); print("SECTION F: CIFAR table and text"); print("=" * 100)
cf = data['cifar']
def msd(recs, key):
    v = np.array([key(r) for r in recs], float); return v.mean(), v.std(ddof=1)
cifar_tab = [
    ('single','nll', 1.9959, 0.0269), ('deepens','nll', 0.7070, 0.0783),
    ('snapshot','nll', 0.8890, 0.0157), ('swa','nll', 1.0740, 0.0173),
    ('single','acc', 0.7086, 0.0052), ('deepens','acc', 0.7786, 0.0081),
    ('snapshot','acc', 0.7466, 0.0044), ('swa','acc', 0.7331, 0.0032),
    ('single','ece15', 0.2213, 0.0037), ('deepens','ece15', 0.0407, 0.0596),
    ('snapshot','ece15', 0.0826, 0.0030), ('swa','ece15', 0.1454, 0.0022),
    ('single','ts.nll', 0.8620, 0.0099), ('deepens','ts.nll', 0.6793, 0.0294),
    ('snapshot','ts.nll', 0.7501, 0.0104), ('swa','ts.nll', 0.7798, 0.0108),
    ('single','auroc_msp_cifar100', 0.6799, 0.0035), ('deepens','auroc_msp_cifar100', 0.7488, 0.0049),
    ('snapshot','auroc_msp_cifar100', 0.7192, 0.0034), ('swa','auroc_msp_cifar100', 0.7046, 0.0026),
    ('deepens','member_mean_nll', 1.0676, 0.1254), ('snapshot','member_mean_nll', 1.2288, 0.0202),
    ('deepens','disagreement_jsd', 0.1545, 0.0614), ('snapshot','disagreement_jsd', 0.0915, 0.0012),
]
def metric_getter(cond, met):
    if met == 'ts.nll':
        return lambda r: r[cond]['ts']['nll']
    return lambda r: r[cond][met]
for cond, met, pm, ps in cifar_tab:
    m, s = msd(cf, metric_getter(cond, met))
    check(f'TabCIFAR {cond}.{met}', f'{pm}±{ps}', f'{m:.4f}±{s:.4f}',
          close(m, pm) and close(s, ps, 0.0006))

cifar_nll = family(cf, lambda r, c: r[c]['nll'])
for c, (pd_, plo, phi) in {('deepens','single'): (-1.2889,-1.3432,-1.2345),
                            ('snapshot','single'): (-1.1069,-1.1281,-1.0856),
                            ('swa','single'): (-0.9219,-0.9448,-0.8990),
                            ('deepens','snapshot'): (-0.1820,-0.2402,-0.1238),
                            ('snapshot','swa'): (-0.1850,-0.1908,-0.1792)}.items():
    m, lo, hi, p, h = cifar_nll[c]
    check(f'TabCIFAR NLL {c[0]}-{c[1]}', f'{pd_:.4f} [{plo:.4f},{phi:.4f}] H=0.0098',
          f'{m:.4f} [{lo:.4f},{hi:.4f}] H={h:.4f}',
          close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006) and abs(h - 0.0098) < 0.0003)

# CIFAR accuracy contrast DE-SG +0.0699 [+0.0627,+0.0772]
d = np.array([r['deepens']['acc'] - r['single']['acc'] for r in cf])
m, lo, hi = t_ci(d)
check('S4.6 text', 'CIFAR DE-SG acc +0.0699 [+0.0627,+0.0772]', f'{m:.4f} [{lo:.4f},{hi:.4f}]',
      close(m, 0.0699) and close(lo, 0.0627, 0.0006) and close(hi, 0.0772, 0.0006))

# CIFAR TS contrast DE-SG -0.1827 adj 0.0098
cifar_ts = family(cf, lambda r, c: r[c]['ts']['nll'])
m, lo, hi, p, h = cifar_ts[('deepens','single')]
check('S4.6 text', 'CIFAR TS DE-SG -0.1827 adj 0.0098', f'{m:.4f} adj={h:.4f}',
      close(m, -0.1827) and abs(h - 0.0098) < 0.0003)

# CIFAR mechanism: member NLL 1.0676 vs 1.2288 (in table above); JSD 0.1545 vs 0.0915 (above)
# fitted temperatures: Single 4.23, SWA 2.30, Snapshot 1.88, DeepEns 1.14
for cond, pt in [('single',4.23),('swa',2.30),('snapshot',1.88),('deepens',1.14)]:
    m, s = msd(cf, lambda r, c=cond: r[c]['ts']['T'])
    check(f'S4.6 T {cond}', f'{pt}', f'{m:.4f}', close(m, pt, 0.006))

# anomalous replicate 8
print(); print("-- CIFAR anomalous replicate 8 --")
r8 = cf[8]
vals = {'deepens nll': r8['deepens']['nll'], 'deepens ece15': r8['deepens']['ece15'],
        'snapshot nll': r8['snapshot']['nll'], 'single nll': r8['single']['nll'],
        'deepens member_mean_acc': r8['deepens']['member_mean_acc'],
        'deepens member_mean_nll': r8['deepens']['member_mean_nll'],
        'deepens jsd': r8['deepens']['disagreement_jsd']}
for k, v in vals.items(): print(f'   seed8 {k} = {v:.4f}')
check('S4.6', 'seed8 DeepEns NLL 0.929, ECE 0.210, member acc 0.515; Snapshot 0.882; Single 2.017',
      f"NLL {vals['deepens nll']:.4f}, ECE {vals['deepens ece15']:.4f}, "
      f"macc {vals['deepens member_mean_acc']:.4f}, SN {vals['snapshot nll']:.4f}, SG {vals['single nll']:.4f}",
      close(vals['deepens nll'], 0.929, 0.0006) and close(vals['deepens ece15'], 0.210, 0.0006)
      and close(vals['deepens member_mean_acc'], 0.515, 0.0006)
      and close(vals['snapshot nll'], 0.882, 0.0006) and close(vals['single nll'], 2.017, 0.0006))
# reversal: DeepEns NLL > Snapshot NLL at seed 8 only
rev = [i for i, r in enumerate(cf) if r['deepens']['nll'] > r['snapshot']['nll']]
check('S4.6', 'exactly one replicate reverses DE-SN ordering (seed level)', f'seeds {rev}', rev == [8])
# uniqueness: other 9 seeds member_mean_acc ~0.72
others = [r['deepens']['member_mean_acc'] for i, r in enumerate(cf) if i != 8]
check('S4.6/report C', 'other nine member acc 0.7257±0.0042',
      f'{np.mean(others):.4f}±{np.std(others, ddof=1):.4f}',
      close(np.mean(others), 0.7257, 0.0006) and close(np.std(others, ddof=1), 0.0042, 0.0006))

# leave-one-out: drop 8 -> DE-SN NLL -0.2075, ECE -0.0607, both P=0.0039
sub = [r for i, r in enumerate(cf) if i != 8]
d = np.array([r['deepens']['nll'] - r['snapshot']['nll'] for r in sub])
m, lo, hi = t_ci(d); p = perm_p(d)
check('S4.6 LOO', 'drop-8 DE-SN NLL -0.2075 P=0.0039', f'{m:.4f} P={p:.4f}',
      close(m, -0.2075, 0.0006) and abs(p - 0.0039) < 0.0003)
d = np.array([r['deepens']['ece15'] - r['snapshot']['ece15'] for r in sub])
m, lo, hi = t_ci(d); p = perm_p(d)
check('S4.6 LOO', 'drop-8 DE-SN ECE -0.0607 P=0.0039', f'{m:.4f} P={p:.4f}',
      close(m, -0.0607, 0.0006) and abs(p - 0.0039) < 0.0003)

# ---------- SWA-dense (Table S2) ----------
print(); print("-- SWA-dense Table S2 --")
sd_recs = load(f'{R}/experiment_swa_dense.jsonl')
# structure check
print('   swa-dense record keys:', list(sd_recs[0].keys()))

import json as _json
with open('/home/z/my-project/v4-work/verify_stage2.json', 'w') as f:
    _json.dump({'n_checks': len(CHECKS), 'n_fail': sum(1 for c in CHECKS if not c[3]),
                'checks': [[str(x) for x in c] for c in CHECKS]}, f, indent=1)
print(f'stage 2: {len(CHECKS)} checks, {sum(1 for c in CHECKS if not c[3])} failures')
