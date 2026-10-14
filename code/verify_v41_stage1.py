#!/usr/bin/env python3
"""
v4.1 audit: independent recomputation of ALL key statistics in the manuscript
from raw per-seed JSONL records. Nothing is taken from the released analysis
JSONs; everything is recomputed and compared against the manuscript's claims.

Outputs a verification table: claim location -> paper value -> recomputed -> verdict.
"""
import json, math, os, itertools
import numpy as np
from scipy import stats as st

R = '/home/z/my-project/v4-work/repo/results'
OUT = []

def load(path):
    recs = []
    with open(path) as f:
        for line in f:
            recs.append(json.loads(line))
    return recs

# ---------- statistical machinery (independent implementation) ----------
def perm_p(diffs):
    """Exact two-sided sign-flip permutation P over 2^n patterns."""
    d = np.asarray(diffs, float)
    n = len(d)
    obs = abs(d.mean())
    cnt = 0
    for mask in range(2 ** n):
        s = d.copy()
        for i in range(n):
            if (mask >> i) & 1:
                s[i] = -s[i]
        if abs(s.mean()) >= obs - 1e-12:
            cnt += 1
    return cnt / (2 ** n)

def t_ci(diffs):
    d = np.asarray(diffs, float)
    n = len(d)
    m = d.mean()
    se = d.std(ddof=1) / math.sqrt(n)
    tc = st.t.ppf(0.975, n - 1)
    return m, m - tc * se, m + tc * se, d.std(ddof=1)

def holm(pvals):
    """Holm-Bonferroni: returns adjusted p-values in original order."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    prev = 0.0
    for rank, idx in enumerate(order):
        a = min(1.0, (m - rank) * p[idx])
        a = max(a, prev)  # enforce monotonicity
        adj[idx] = a
        prev = a
    return adj

CONTRASTS = [
    ('deepens', 'single'), ('snapshot', 'single'), ('swa', 'single'),
    ('deepens', 'snapshot'), ('snapshot', 'swa'),
]

def contrasts_for(recs, metric_fn, family_holm=True):
    """Returns dict contrast -> (mean, lo, hi, p_raw, p_holm)."""
    out = {}
    vals = {}
    for (a, b) in CONTRASTS:
        da = np.array([metric_fn(r, a) for r in recs], float)
        db = np.array([metric_fn(r, b) for r in recs], float)
        diffs = da - db
        m, lo, hi, sd = t_ci(diffs)
        p = perm_p(diffs)
        vals[(a, b)] = (m, lo, hi, p, sd)
    if family_holm:
        ps = [vals[c][3] for c in CONTRASTS]
        hs = holm(ps)
        for c, h in zip(CONTRASTS, hs):
            m, lo, hi, p, sd = vals[c]
            vals[c] = (m, lo, hi, p, h)
    return vals

def msd(recs, metric_fn, cond):
    v = np.array([metric_fn(r, cond) for r in recs], float)
    return v.mean(), v.std(ddof=1)

# ---------- claim registry ----------
CHECKS = []  # (location, claim, recomputed_str, ok)
def check(loc, claim, value, ok):
    CHECKS.append((loc, claim, value, ok))
    print(f"[{'OK ' if ok else 'FAIL'}] {loc}: claimed {claim} | recomputed {value}")

def close(a, b, tol=0.0005):
    return abs(a - b) <= tol

def fmt(x):
    if isinstance(x, str): return x
    return f"{x:.4f}"

# ---------- load all settings ----------
files = {
    'core':  f'{R}/v2/experiment_v2_fmnist_B60_k3.jsonl',
    'B30':   f'{R}/v2/experiment_v2_fmnist_B30_k3.jsonl',
    'B120':  f'{R}/v2/experiment_v2_fmnist_B120_k3.jsonl',
    'k5':    f'{R}/v2/experiment_v2_fmnist_B60_k5.jsonl',
    'mnist': f'{R}/v2/experiment_v2_mnist_B60_k3.jsonl',
    'cifar': f'{R}/cifar/experiment_cifar_B60_k3.jsonl',
    'v1core': f'{R}/experiment.jsonl',
    'swadense': f'{R}/experiment_swa_dense.jsonl',
}
data = {k: load(v) for k, v in files.items()}

# probe suffix helper: v2 MLP files use auroc_msp_<probe>; cifar uses auroc_msp_cifar100; v1 core uses auroc_msp (MNIST)
def m_nll(r, c): return r[c]['nll']
def m_acc(r, c): return r[c]['acc']
def m_brier(r, c): return r[c]['brier']
def m_ece15(r, c): return r[c]['ece15']
def m_ts_nll(r, c): return r[c]['ts']['nll']
def m_T(r, c): return r[c]['ts']['T']

print("=" * 100)
print("SECTION A: Table 1 (core setting condition summaries) + v1/v2 consistency")
print("=" * 100)
core = data['core']; v1 = data['v1core']
assert len(core) == 10 and len(v1) == 10

# v1 vs v2 bit-consistency on shared metrics (all 10 seeds)
mismatch = 0
for s in range(10):
    r2, r1 = core[s], v1[s]
    for cond in ['single', 'deepens', 'snapshot', 'swa']:
        for met in ['nll', 'acc', 'brier', 'ece15']:
            if abs(r2[cond][met] - r1[cond][met]) > 1e-12: mismatch += 1
        # v1 auroc_msp is MNIST probe
        if abs(r2[cond]['auroc_msp_mnist'] - r1[cond]['auroc_msp']) > 1e-12: mismatch += 1
check('S3.6 Repro', 'v2 pipeline reproduces v1 records (bit-level, 10 seeds x 4 cond x 5 metrics)',
      f'{mismatch} mismatches of 200 comparisons', mismatch == 0)

tab1 = {  # paper Table 1
    ('single','nll'): (0.5265, 0.0159), ('deepens','nll'): (0.3020, 0.0019),
    ('snapshot','nll'): (0.3485, 0.0067), ('swa','nll'): (0.3868, 0.0085),
    ('single','acc'): (0.8895, 0.0015), ('deepens','acc'): (0.8965, 0.0012),
    ('snapshot','acc'): (0.8935, 0.0015), ('swa','acc'): (0.8926, 0.0018),
    ('single','brier'): (0.1796, 0.0020), ('deepens','brier'): (0.1504, 0.0011),
    ('snapshot','brier'): (0.1596, 0.0024), ('swa','brier'): (0.1646, 0.0028),
    ('single','ece15'): (0.0702, 0.0021), ('deepens','ece15'): (0.0236, 0.0008),
    ('snapshot','ece15'): (0.0444, 0.0025), ('swa','ece15'): (0.0517, 0.0025),
    ('deepens','member_mean_nll'): (0.3379, 0.0022), ('snapshot','member_mean_nll'): (0.4039, 0.0087),
    ('deepens','disagreement_jsd'): (0.0150, 0.0003), ('snapshot','disagreement_jsd'): (0.0106, 0.0003),
}
fns = {'nll': m_nll, 'acc': m_acc, 'brier': m_brier, 'ece15': m_ece15,
       'member_mean_nll': lambda r, c: r[c]['member_mean_nll'],
       'disagreement_jsd': lambda r, c: r[c]['disagreement_jsd']}
for (cond, met), (pm, ps) in tab1.items():
    m, s = msd(core, fns[met], cond)
    check(f'Tab1 {cond}.{met}', f'{pm:.4f}±{ps:.4f}', f'{m:.4f}±{s:.4f}',
          close(m, pm) and close(s, ps, 0.0006))

# AUROC table 1: MNIST and KMNIST probes + entropy
tab1_auroc = {
    ('single','auroc_msp_mnist'): (0.7533, 0.0172), ('deepens','auroc_msp_mnist'): (0.8502, 0.0049),
    ('snapshot','auroc_msp_mnist'): (0.7956, 0.0139), ('swa','auroc_msp_mnist'): (0.7504, 0.0168),
    ('single','auroc_msp_kmnist'): (0.6951, 0.0184), ('deepens','auroc_msp_kmnist'): (0.8048, 0.0067),
    ('snapshot','auroc_msp_kmnist'): (0.7536, 0.0131), ('swa','auroc_msp_kmnist'): (0.7063, 0.0132),
    ('single','auroc_ent_mnist'): (0.7562, 0.0172), ('deepens','auroc_ent_mnist'): (0.8657, 0.0055),
    ('snapshot','auroc_ent_mnist'): (0.8059, 0.0144), ('swa','auroc_ent_mnist'): (0.7573, 0.0171),
}
for (cond, met), (pm, ps) in tab1_auroc.items():
    v = np.array([r[cond][met] for r in core], float)
    check(f'Tab1 {cond}.{met}', f'{pm:.4f}±{ps:.4f}', f'{v.mean():.4f}±{v.std(ddof=1):.4f}',
          close(v.mean(), pm) and close(v.std(ddof=1), ps, 0.0006))

print()
print("=" * 100)
print("SECTION B: Table 2 (core NLL contrasts)")
print("=" * 100)
core_nll = contrasts_for(core, m_nll)
tab2 = {('deepens','single'): (-0.2245, -0.2360, -0.2130, 0.0020, 0.0098),
        ('snapshot','single'): (-0.1780, -0.1902, -0.1658, 0.0020, 0.0098),
        ('swa','single'): (-0.1396, -0.1514, -0.1279, 0.0020, 0.0098),
        ('deepens','snapshot'): (-0.0465, -0.0505, -0.0425, 0.0020, 0.0098),
        ('snapshot','swa'): (-0.0384, -0.0407, -0.0360, 0.0020, 0.0098)}
for c, (pd_, plo, phi, pp, ph) in tab2.items():
    m, lo, hi, p, h = core_nll[c][:5]
    check(f'Tab2 {c[0]}-{c[1]}', f'{pd_:.4f} [{plo:.4f},{phi:.4f}] P={pp} Holm={ph}',
          f'{m:.4f} [{lo:.4f},{hi:.4f}] P={p:.4f} Holm={h:.4f}',
          close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006)
          and abs(p - pp) < 0.0003 and abs(h - ph) < 0.0003)

# sign unanimity claim: all ten replicates favoured every strategy over Single for NLL
allpos = all((r['deepens']['nll'] - r['single']['nll']) < 0 and
             (r['snapshot']['nll'] - r['single']['nll']) < 0 and
             (r['swa']['nll'] - r['single']['nll']) < 0 for r in core)
check('S4.1', 'all ten replicates favoured every strategy over Single (NLL)',
      str(allpos), allpos)

print()
print("=" * 100)
print("SECTION C: Table 3/tab:extension (NLL contrasts vs Single, extension settings)")
print("=" * 100)
ext = {
    'B30':  {'deepens': (-0.0754, -0.0809, -0.0699, 0.0098), 'snapshot': (-0.0671, -0.0736, -0.0606, 0.0098), 'swa': (-0.0530, -0.0587, -0.0473, 0.0098)},
    'B120': {'deepens': (-0.3317, -0.3416, -0.3219, 0.0098), 'snapshot': (-0.2283, -0.2377, -0.2188, 0.0098), 'swa': (-0.1552, -0.1658, -0.1446, 0.0098)},
    'k5':   {'deepens': (-0.2290, -0.2410, -0.2171, 0.0098), 'snapshot': (-0.2035, -0.2142, -0.1928, 0.0098), 'swa': (-0.1673, -0.1765, -0.1581, 0.0098)},
    'mnist': {'deepens': (-0.0158, -0.0183, -0.0134, 0.0098), 'snapshot': (-0.0015, -0.0042, 0.0012, 0.41), 'swa': (0.0017, -0.0012, 0.0046, 0.41)},
}
for setting, conds in ext.items():
    res = contrasts_for(data[setting], m_nll)
    for cond, (pd_, plo, phi, ph) in conds.items():
        m, lo, hi, p, h = res[(cond, 'single')]
        ok = close(m, pd_) and close(lo, plo, 0.0006) and close(hi, phi, 0.0006) and abs(h - ph) < 0.011
        check(f'Tab3 {setting} {cond}-single', f'{pd_:.4f} [{plo:.4f},{phi:.4f}] Holm={ph}',
              f'{m:.4f} [{lo:.4f},{hi:.4f}] Holm={h:.4f}', ok)

# MNIST-direction within-strategy contrasts (text: DE-SN -0.0143 adj 0.0098; SN-SWA sig)
res_m = contrasts_for(data['mnist'], m_nll)
m, lo, hi, p, h = res_m[('deepens', 'snapshot')]
check('S4.2 text', 'MNIST DE-SN NLL -0.0143 adj P=0.0098', f'{m:.4f} adj P={h:.4f}',
      close(m, -0.0143) and abs(h - 0.0098) < 0.0003)
m, lo, hi, p, h = res_m[('snapshot', 'swa')]
check('S4.2 text', 'MNIST SN-SWA significant adj 0.0098', f'{m:.4f} adj P={h:.4f}', h < 0.05)

# NEW ANALYSIS 1: DeepEns - SWA direct contrast on MNIST NLL (replaces 'by adjacency')
d_deswa = np.array([r['deepens']['nll'] - r['swa']['nll'] for r in data['mnist']])
m_, lo_, hi_, sd_ = t_ci(d_deswa); p_ = perm_p(d_deswa)
check('NEW (S4.2 fix)', 'MNIST DE-SWA direct NLL contrast (paper says "by adjacency")',
      f'{m_:.4f} [{lo_:.4f},{hi_:.4f}] P={p_:.4f}', True)

# MNIST direction condition means (text: acc 0.982, ECE 0.0098 for Single)
a_m, a_s = msd(data['mnist'], m_acc, 'single')
e_m, e_s = msd(data['mnist'], m_ece15, 'single')
check('S4.2 text', 'MNIST Single acc 0.982, ECE 0.0098', f'acc {a_m:.4f}, ECE {e_m:.4f}',
      close(a_m, 0.982, 0.0006) and close(e_m, 0.0098, 0.0006))

# NEW ANALYSIS 2: ECE mean ordering in ALL settings (abstract claim 'ordering robust')
print("\n-- ECE means by setting (for abstract ordering claim) --")
for setting in ['core', 'B30', 'B120', 'k5', 'mnist', 'cifar']:
    ems = {c: msd(data[setting], m_ece15, c) for c in ['single', 'deepens', 'snapshot', 'swa']}
    ordered = ems['deepens'][0] < ems['snapshot'][0] < ems['swa'][0] < ems['single'][0]
    print(f"  {setting:6s}: DE {ems['deepens'][0]:.4f} SN {ems['snapshot'][0]:.4f} "
          f"SWA {ems['swa'][0]:.4f} SG {ems['single'][0]:.4f}  strict-order={ordered}")
    check(f'ordering ECE {setting}', 'DE<SN<SWA<SG in means', 'computed above', ordered)

print()
print("=" * 100)
print("SECTION D: Temperature scaling (S4.3, Table S3, fig3)")
print("=" * 100)
# core TS
ts_core = contrasts_for(core, m_ts_nll)
m, lo, hi, p, h = ts_core[('deepens', 'single')]
check('S4.3', 'core TS DE-SG -0.0434 [-0.0468,-0.0400] Holm 0.0098',
      f'{m:.4f} [{lo:.4f},{hi:.4f}] Holm={h:.4f}',
      close(m, -0.0434) and close(lo, -0.0468, 0.0006) and close(hi, -0.0400, 0.0006))
# Single TS: NLL 0.3325, ECE 0.0111; DeepEns TS-NLL 0.2891±0.0020
sn_ts = msd(core, m_ts_nll, 'single')
de_ts = msd(core, m_ts_nll, 'deepens')
se_ts = msd(core, lambda r, c: r[c]['ts']['ece15'], 'single')
check('S4.3', 'Single TS-NLL 0.3325', f'{sn_ts[0]:.4f}', close(sn_ts[0], 0.3325))
check('S4.3', 'Single TS-ECE 0.0111', f'{se_ts[0]:.4f}', close(se_ts[0], 0.0111))
check('S4.3', 'DeepEns TS-NLL 0.2891±0.0020', f'{de_ts[0]:.4f}±{de_ts[1]:.4f}',
      close(de_ts[0], 0.2891) and close(de_ts[1], 0.0020, 0.0006))
# fitted T ordering: Single 2.46, SWA 1.79, Snapshot 1.58, DeepEns 1.25
for cond, pt in [('single', 2.46), ('swa', 1.79), ('snapshot', 1.58), ('deepens', 1.25)]:
    tm, tstd = msd(core, m_T, cond)
    check(f'S4.3 T {cond}', f'mean T = {pt}', f'{tm:.4f}', close(tm, pt, 0.006))
# B30 TS: spans 0.2986-0.3126, snapshot nominally best, DE-SN +0.0026 [+0.0002,+0.0050] adj 0.045
ts_b30 = {c: msd(data['B30'], m_ts_nll, c)[0] for c in ['single','deepens','snapshot','swa']}
check('S4.3', 'B30 TS-NLL ensemble span 0.2986-0.3126, Snapshot best',
      f"span {min(ts_b30['deepens'],ts_b30['snapshot'],ts_b30['swa']):.4f}-"
      f"{max(ts_b30['deepens'],ts_b30['snapshot'],ts_b30['swa']):.4f}, best={min(ts_b30, key=ts_b30.get)}",
      close(min(ts_b30.values()), 0.2986, 0.0006) and close(max(ts_b30.values()), 0.3126, 0.0006)
      and min(ts_b30, key=ts_b30.get) == 'snapshot')
ts_b30c = contrasts_for(data['B30'], m_ts_nll)
m, lo, hi, p, h = ts_b30c[('deepens', 'snapshot')]
check('S4.3', 'B30 TS DE-SN +0.0026 [+0.0002,+0.0050] adj 0.045',
      f'{m:.4f} [{lo:.4f},{hi:.4f}] adj={h:.4f}',
      close(m, 0.0026) and close(lo, 0.0002, 0.0006) and close(hi, 0.0050, 0.0006)
      and abs(h - 0.045) < 0.006)
# Table S3 rows: TS-NLL vs single, Holm per setting's TS family
tabS3 = {('core','deepens'): (-0.0434, 0.0098), ('core','snapshot'): (-0.0314, 0.0098),
         ('B30','deepens'): (-0.0114, 0.0098), ('B30','snapshot'): (-0.0140, 0.0098),
         ('B120','deepens'): (-0.0567, 0.0098), ('B120','snapshot'): (-0.0349, 0.0098),
         ('k5','deepens'): (-0.0384, 0.0098), ('k5','snapshot'): (-0.0374, 0.0098),
         ('mnist','deepens'): (-0.0071, 0.0098), ('mnist','snapshot'): (-0.0016, 0.0625)}
for (setting, cond), (pd_, ph) in tabS3.items():
    res = contrasts_for(data[setting], m_ts_nll)
    m, lo, hi, p, h = res[(cond, 'single')]
    check(f'TabS3 {setting} {cond}', f'{pd_:.4f} Holm={ph}', f'{m:.4f} Holm={h:.4f}',
          close(m, pd_) and abs(h - ph) < 0.011)

# TS effect on OOD AUROC (per condition): digit max |delta| and CIFAR values
def ts_ood_delta(recs, cond, probe):
    v = [r[cond]['ts'][f'auroc_msp_{probe}'] - r[cond][f'auroc_msp_{probe}'] for r in recs]
    return np.mean(v)
digit_max = 0.0
for setting, probes in [('core', ['mnist','kmnist']), ('B30', ['mnist','kmnist']),
                        ('B120', ['mnist','kmnist']), ('k5', ['mnist','kmnist']),
                        ('mnist', ['fmnist','kmnist'])]:
    for probe in probes:
        for cond in ['single','deepens','snapshot','swa']:
            digit_max = max(digit_max, abs(ts_ood_delta(data[setting], cond, probe)))
check('S4.3', 'digit tasks: TS changes OOD AUROC by at most +0.012', f'max |delta| = {digit_max:.4f}',
      close(digit_max, 0.0119, 0.0002))
for cond, pv in [('single', 0.026), ('swa', 0.019), ('snapshot', 0.017), ('deepens', 0.004)]:
    d = ts_ood_delta(data['cifar'], cond, 'cifar100')
    check(f'S4.3 CIFAR TS-OOD {cond}', f'+{pv}', f'+{d:.4f}', close(d, pv, 0.0006))
# gap compression 0.069 -> 0.046
g_raw = np.mean([r['deepens']['auroc_msp_cifar100'] - r['single']['auroc_msp_cifar100'] for r in data['cifar']])
g_ts = np.mean([(r['deepens']['ts']['auroc_msp_cifar100'] - r['single']['ts']['auroc_msp_cifar100']) for r in data['cifar']])
check('S4.3', 'CIFAR DE-SG OOD gap +0.069 -> +0.046 after TS', f'{g_raw:.4f} -> {g_ts:.4f}',
      close(g_raw, 0.069, 0.0006) and close(g_ts, 0.046, 0.0006))
# examples: Single 0.7533->0.7620 (MNIST probe), DeepEns 0.8502->0.8566
sm = np.mean([r['single']['auroc_msp_mnist'] for r in core]); smt = np.mean([r['single']['ts']['auroc_msp_mnist'] for r in core])
dm = np.mean([r['deepens']['auroc_msp_mnist'] for r in core]); dmt = np.mean([r['deepens']['ts']['auroc_msp_mnist'] for r in core])
check('S4.3', 'Single 0.7533->0.7620 (MNIST probe)', f'{sm:.4f}->{smt:.4f}',
      close(sm, 0.7533) and close(smt, 0.7620, 0.0006))
check('S4.3', 'DeepEns 0.8502->0.8566', f'{dm:.4f}->{dmt:.4f}',
      close(dm, 0.8502) and close(dmt, 0.8566, 0.0006))

# save intermediate results for later phases
with open('/home/z/my-project/v4-work/verify_stage1.json', 'w') as f:
    json.dump({'n_checks': len(CHECKS), 'n_fail': sum(1 for c in CHECKS if not c[3]),
               'checks': [[str(x) for x in c] for c in CHECKS]}, f, indent=1)
print(f"\n=== STAGE 1: {len(CHECKS)} checks, {sum(1 for c in CHECKS if not c[3])} failures ===")
