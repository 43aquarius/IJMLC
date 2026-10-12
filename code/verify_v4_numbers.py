#!/usr/bin/env python3
"""Verify every number added/changed in the v4 manuscript against the
independent re-analysis (reanalysis_v4.json) and the diagnostic record."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
rep = json.load(open(os.path.join(REPO, 'results', 'v4', 'reanalysis_v4.json')))
diag = json.load(open(os.path.join(REPO, 'results', 'v4', 'seed8_diagnosis.json')))
tex = open(os.path.join(REPO, 'manuscript-source', 'main.tex')).read()

checks = []
def chk(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

S = rep['settings']

def c(setting, contrast, metric, key='mean_delta'):
    return S[setting]['contrasts'][contrast][metric][key]

def raw(setting, contrast, metric):
    return S[setting]['contrasts'][contrast][metric]['p_perm_exact']

def hol(setting, probe, contrast):
    return S[setting]['holm'][f'Oa_msp_{probe}'][contrast]

# --- Abstract ---
chk("abstract SWA OOD range -0.016..+0.025",
    abs(c('fmnist_B120_k3','swa_vs_single','auroc_msp_mnist') - (-0.0157)) < 5e-4 and
    abs(c('cifar10_B60_k3','swa_vs_single','auroc_msp_cifar100') - 0.0247) < 5e-4)
chk("abstract TS NLL 0.289/0.333",
    abs(S['fmnist_B60_k3']['metrics_by_condition']['ts.nll']['deepens']['mean'] - 0.2891) < 5e-4 and
    abs(S['fmnist_B60_k3']['metrics_by_condition']['ts.nll']['single']['mean'] - 0.3325) < 5e-4)

# --- section 4.3 TS-OOD ---
tsd = S['fmnist_B60_k3']['ts_effect_on_ood']
digit_max = max(v['mean_delta'] for s in ['fmnist_B60_k3','fmnist_B30_k3','fmnist_B120_k3','fmnist_B60_k5','mnist_B60_k3'] for v in rep['settings'][s]['ts_effect_on_ood'].values())
chk("digit TS-OOD max = +0.012", abs(digit_max - 0.0119) < 5e-4, f"actual max {digit_max:.4f}")
ct = S['cifar10_B60_k3']['ts_effect_on_ood']
chk("CIFAR TS-OOD single +0.026", abs(ct['single|cifar100']['mean_delta'] - 0.0260) < 5e-4)
chk("CIFAR TS-OOD swa +0.019", abs(ct['swa|cifar100']['mean_delta'] - 0.0186) < 5e-4, f"actual {ct['swa|cifar100']['mean_delta']:.4f}")
chk("CIFAR TS-OOD snapshot +0.017", abs(ct['snapshot|cifar100']['mean_delta'] - 0.0165) < 5e-4)
chk("CIFAR TS-OOD deepens +0.004", abs(ct['deepens|cifar100']['mean_delta'] - 0.0035) < 5e-4)
gap_raw = c('cifar10_B60_k3','deepens_vs_single','auroc_msp_cifar100')
gap_ts = c('cifar10_B60_k3','deepens_vs_single','ts.auroc_msp_cifar100')
chk("CIFAR DE-SG gap +0.069 -> +0.046", abs(gap_raw-0.0689)<5e-4 and abs(gap_ts-0.0465)<5e-4)

# --- section 4.4 ---
swa_deltas = []
for s in S:
    for m in S[s]['contrasts']['swa_vs_single']:
        if m.startswith('auroc_msp_'):
            swa_deltas.append(S[s]['contrasts']['swa_vs_single'][m]['mean_delta'])
chk("SWA OOD range in text -0.016..+0.025",
    abs(min(swa_deltas) + 0.0157) < 5e-4 and abs(max(swa_deltas) - 0.0247) < 5e-4,
    f"min {min(swa_deltas):.4f} max {max(swa_deltas):.4f}")
# counts
de_sig = sum(1 for s in S for p in [m[10:] for m in S[s]['contrasts']['deepens_vs_single'] if m.startswith('auroc_msp_')] if hol(s,p,'deepens_vs_single') < 0.05)
sn_sig = sum(1 for s in S for p in [m[10:] for m in S[s]['contrasts']['snapshot_vs_single'] if m.startswith('auroc_msp_')] if hol(s,p,'snapshot_vs_single') < 0.05)
swa_sig_pos = sum(1 for s in S for p in [m[10:] for m in S[s]['contrasts']['swa_vs_single'] if m.startswith('auroc_msp_')]
                  if hol(s,p,'swa_vs_single') < 0.05 and S[s]['contrasts']['swa_vs_single'][f'auroc_msp_{p}']['mean_delta'] > 0)
swa_sig_neg = sum(1 for s in S for p in [m[10:] for m in S[s]['contrasts']['swa_vs_single'] if m.startswith('auroc_msp_')]
                  if hol(s,p,'swa_vs_single') < 0.05 and S[s]['contrasts']['swa_vs_single'][f'auroc_msp_{p}']['mean_delta'] < 0)
chk("DeepEns sig on 11/11", de_sig == 11)
chk("Snapshot sig on 9/11", sn_sig == 9)
chk("SWA sig pos 5, neg 1", swa_sig_pos == 5 and swa_sig_neg == 1,
    f"pos={swa_sig_pos} neg={swa_sig_neg}")
de_maxholm = max(hol(s,p,'deepens_vs_single') for s in S for p in [m[10:] for m in S[s]['contrasts']['deepens_vs_single'] if m.startswith('auroc_msp_')])
chk("DeepEns Holm <= 0.031", abs(de_maxholm - 0.0312) < 5e-4, f"{de_maxholm}")
chk("core kmnist SWA +0.0112 Holm 0.023",
    abs(c('fmnist_B60_k3','swa_vs_single','auroc_msp_kmnist') - 0.0112) < 5e-4 and
    abs(hol('fmnist_B60_k3','kmnist','swa_vs_single') - 0.0234) < 5e-4)
chk("B120 mnist SWA -0.016 Holm 0.012",
    abs(c('fmnist_B120_k3','swa_vs_single','auroc_msp_mnist') - (-0.0157)) < 5e-4 and
    abs(hol('fmnist_B120_k3','mnist','swa_vs_single') - 0.0117) < 5e-4)
# entropy range
ent = [S[s]['contrasts']['swa_vs_single'][m]['mean_delta'] for s in S for m in S[s]['contrasts']['swa_vs_single'] if m.startswith('auroc_ent_')]
chk("SWA entropy range -0.015..+0.031", abs(min(ent)+0.0147)<5e-4 and abs(max(ent)-0.0306)<5e-4)
# global family
oc = rep['notes']['Oc_global_msp']
chk("global family size 55, none survive", oc['family_size']==55 and all(v>=0.05 for v in oc['results'].values()))

# --- section 4.6 ---
chk("CIFAR DE-SN ECE -0.0418 CI P=0.082",
    abs(c('cifar10_B60_k3','deepens_vs_snapshot','ece15') + 0.0418) < 5e-4 and
    abs(S['cifar10_B60_k3']['contrasts']['deepens_vs_snapshot']['ece15']['ci95_low'] + 0.0845) < 5e-4 and
    abs(S['cifar10_B60_k3']['contrasts']['deepens_vs_snapshot']['ece15']['ci95_high'] - 0.0008) < 5e-4 and
    abs(raw('cifar10_B60_k3','deepens_vs_snapshot','ece15') - 0.0820) < 5e-4)
chk("CIFAR DE-SG ECE -0.1805 P=0.0020",
    abs(c('cifar10_B60_k3','deepens_vs_single','ece15') + 0.1805) < 5e-4 and
    abs(raw('cifar10_B60_k3','deepens_vs_single','ece15') - 0.0020) < 5e-4)
chk("CIFAR SWA OOD +0.0247 raw 0.0020 hol 0.0098",
    abs(gap_raw*0 + c('cifar10_B60_k3','swa_vs_single','auroc_msp_cifar100') - 0.0247) < 5e-4 and
    abs(raw('cifar10_B60_k3','swa_vs_single','auroc_msp_cifar100') - 0.0020) < 5e-4 and
    abs(hol('cifar10_B60_k3','cifar100','swa_vs_single') - 0.0098) < 5e-4)
# LOO drop-8
loo = rep['notes']['cifar_leave_one_out']['drop_seed8']
chk("LOO drop-8 DE-SN NLL -0.2075 P<=0.0039",
    abs(loo['deepens_vs_snapshot|nll']['mean_delta'] + 0.2075) < 5e-4 and abs(loo['deepens_vs_snapshot|nll']['p_perm_exact'] - 0.0039) < 1e-4)
chk("LOO drop-8 DE-SN ECE -0.0607 P<=0.0039",
    abs(loo['deepens_vs_snapshot|ece15']['mean_delta'] + 0.0607) < 5e-4 and abs(loo['deepens_vs_snapshot|ece15']['p_perm_exact'] - 0.0039) < 1e-4)
# diagnostic
chk("seed8 member acc 0.515 ens 0.929 ece 0.210 (text)",
    "0.515" in tex and "0.929" in tex and "0.210" in tex)
chk("diagnostic: collapsed member NLL~ln10, acc~0.10",
    abs(diag['members']['member2(m1,seed10812)']['test_nll'] - 2.3026) < 5e-3 and
    abs(diag['members']['member2(m1,seed10812)']['test_acc'] - 0.1000) < 5e-4)
chk("diagnostic: shared member matches released history",
    all(abs(diag['members']['member1(shared,seed10800)']['history'][i]['train_loss'] -
            json.loads(open(os.path.join(REPO, 'results', 'cifar', 'experiment_cifar_B60_k3.jsonl')).readlines()[8])['histories']['cyclic'][i]['train_loss']) < 5e-5
        for i in range(20)))
chk("seed8 single NLL 2.017 (text 2.017)",
    abs(json.loads(open(os.path.join(REPO, 'results', 'cifar', 'experiment_cifar_B60_k3.jsonl')).readlines()[8])['single']['nll'] - 2.0171) < 5e-4)

# --- forbidden phrases must be gone ---
for phrase in ["no improvement surviving multiple-comparison correction",
               "Only prediction averaging improved",
               "not their ranking across inputs",
               "bought no shift robustness",
               "tracks \\single{} throughout"]:
    chk(f"forbidden phrase absent: {phrase[:40]}", phrase not in tex)

# --- Table S4 rows: spot-verify against reanalysis ---
s4 = re.findall(r'\$(\+\d\.\d{4}|-\d\.\d{4})\$ & \$\[([+\-\d.,]+)\]\$ & (\d\.\d{4}) & (\d\.\d{4})', tex)
chk("Table S4 has 33 data rows", len(s4) == 33, f"found {len(s4)}")
# verify each S4 row value appears in the reanalysis
reanalysis_vals = set()
for s in S:
    for t in S[s]['contrasts']:
        for m in S[s]['contrasts'][t]:
            if m.startswith('auroc_msp_'):
                d = S[s]['contrasts'][t][m]
                reanalysis_vals.add(f"{d['mean_delta']:+.4f}")
                reanalysis_vals.add(f"{d['p_perm_exact']:.4f}")
missing = [r[0] for r in s4 if r[0] not in reanalysis_vals]
chk("all S4 deltas match reanalysis", not missing, f"missing: {missing[:5]}")
hp = [r[3] for r in s4 if r[1] and r[3]]
chk("S4 Holm values plausible", all(0 < float(x) <= 1 for x in hp))

fails = [c for c in checks if not c[1]]
print(f"{len(checks)-len(fails)}/{len(checks)} checks PASS")
for name, ok, detail in fails:
    print("FAIL:", name, detail)
sys.exit(1 if fails else 0)
