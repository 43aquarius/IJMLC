# Revision Log v2 → v3 (Deliverable F)

**Manuscript:** "Deep ensembles outperform snapshot ensembles and weight averaging
for calibrated uncertainty under fixed training budgets" (v3, 12 October 2026)
**Previous version:** v2 (19 pp., 11 October 2026). "v3 location" refers to the
section numbering of the v3 manuscript.

| # | Issue (v2) | Fix (v3) | v3 location | Basis / evidence | New experiment? | Verification |
|---|------------|----------|-------------|------------------|-----------------|--------------|
| V3-01 (P1) | Abstract + §4.2 claimed the DeepEns>Snap>SWA>Single ordering on "every in-distribution metric", robust across budgets | Ordering claim scoped to **NLL and ECE**; the B=30 and k=5 secondary-metric exceptions reported explicitly with values (acc: Snapshot 0.8929 > Single 0.8917 > SWA 0.8914 > DeepEns 0.8905 at B=30, DeepEns−Single −0.0012 [−0.0021,−0.0002] p=0.018; Brier Snapshot 0.1562 < DeepEns 0.1573; k=5 acc Snapshot 0.8944 > DeepEns 0.8938; all reversals ≤0.003, never NLL/ECE) | Abstract; §4.2 new paragraph | analysis_v2.json (this audit, 100+ value diff) | No | verify_claims_v3.py diff vs manuscript; manual read |
| V3-02 (P1) | §4.3 "the same two conclusions held in every extension setting" — false at B=30 post-TS (Snapshot significantly better than DeepEns on TS-NLL: +0.0026 [+0.0002,+0.0050], p_holm=0.045) | Rewritten: DeepEns vs Single significant everywhere, but at B=30 TS "largely equalised the ensemble strategies" with Snapshot nominally best and the DeepEns−Snapshot contrast reversed; the honest two-sided reading is kept and connected to the practical guidance | §4.3 ¶2; §5 recalibration paragraph | analysis_v2.json fmnist_B30_k3 ts.nll contrasts | No | values re-diffed |
| V3-03 (P1) | No cross-architecture evidence (MLP-only) | **CIFAR-10 + SmallCNN extension executed** (B=60, k=3, 10 seeds, post-hoc-labelled, plan pre-specified before evaluation); new Results section, Fig. 5, Table 4; Intro/Abstract/Discussion/Conclusion updated; Limitations rewritten | §4.6; Fig. 5; Table 4; Abstract; §1; §5; §5.1; §6 | results/cifar/experiment_cifar_B60_k3.jsonl + analysis_cifar.json | **Yes** (CIFAR run) | numbers filled programmatically from analysis_cifar.json; independent permutation recomputation |
| V3-04 (P1) | Title scope broader than evidence | Title changed to "…under fixed training budgets"; two candidate titles compared and rejected (see §below) | Title block; \hypersetup | audit reasoning (§10.1 of directive) | No | manual |
| V3-05 (P2) | Training budget vs wall-clock vs inference vs deployment cost conflated | New four-dimension cost paragraph in Methods; inference-cost caveat added to practitioner guidance and Limitations | §3.1 final paragraph; §5 guidance; §5.1 | code-level budget audit (identical update counts verified) | No | code audit |
| V3-06 (P2) | Garbled sentence "The ensemble effect that longer training damages calibration and averaging repairs it---requires headroom…" | Rewritten with correct em-dash structure and associational wording ("is observed only where such damage exists") | §4.2 ¶3 | copy-edit | No | manual |
| V3-07 (P2) | MNIST-direction OOD P values not labelled uncorrected in that sentence | "(uncorrected as above)" added; "OOD contrasts are secondary" stated at first use in §4.4 | §4.4 ¶1–2 | analysis conventions | No | manual |
| V3-08 (P2) | "include most practically deployed under-trained or heavily optimised classifiers" — uncited external claim | Replaced by hedged statement + concrete verification recipe ("a single reliability diagram suffices") | §5 ¶3 | audit | No | manual |
| V3-09 (P2) | Abstract/§4.4 "SWA showed no reliable improvement" could be read as a proved null | "no improvement surviving multiple-comparison correction" (abstract, contributions, conclusion); §4.4 reports the one uncorrected exception with its size and the absence-of-evidence caveat (kept) | Abstract; §1 bullets; §4.4; §6 | analysis_v2.json | No | manual |
| V3-10 (P3) | thebibliography count argument (22) vs 21 entries | Corrected (24 after additions) | references | compile check | No | compile |
| V3-11 (P2) | 2024–2026 coverage thin | Three verified references added: Ajroldi et al. (ICML 2025), Chirkova et al. (2020), Thuy & Benoit (Ann. Oper. Res. 2024) + positioning sentences; Positioning paragraph updated with the 2024–2025 re-check statement | §2 (three paragraphs) | literature re-check (litsearch_v3 logs; OpenReview API + Crossref verification) | No | bibliographic verification logged |
| V3-12 (P3) | "improved every strategy" (k=5) while Single is unchanged by construction | "improved every ensemble strategy (Single is unchanged by construction)" | §4.2 ¶1 | analysis_v2.json (single NLL identical across k) | No | value check |
| New (P0-check) | User-reported "AI-generated" watermark on p.19 | Investigated: **not present in the manuscript file** (text layer, raw content streams, 110/200-dpi visual inspection, GitHub release asset MD5-identical). Concluded viewer-added artefact; documented; no source change required; release PDF re-verified after rebuild | audit-report-v3.md §1.4 | 4-layer verification | No | documented |
| New (P2) | Code repo not usable from a clean clone (hard-coded paths; missing torchvision dep) | paths.py refactor; torchvision-free KMNIST download; requirements update; README rewritten | repo code/ + README | clean-clone test | No | **clean-env gate: 110/110 values bit-identical** |
| New (P1) | Statistical machinery independently re-verified | verify_claims_v3.py re-enumerates all 2^10 sign-flip permutation tests from per-seed deltas; all match; 100+ manuscript values diffed against analysis JSON | research-docs/audit-report-v3.md | this audit | No | PASS |

## Title decision (directive §10.1)

Candidates considered:
1. *"Budget-split deep ensembles outperform snapshot ensembles and weight
   averaging for calibrated uncertainty under fixed training budgets"* —
   accurate but redundant ("budget-split…budgets").
2. *"How to spend a fixed training budget: deep ensembles versus snapshot
   ensembles and weight averaging for calibrated uncertainty"* — engaging,
   but longer and question-style titles can read as overclaiming in journal
   context.
3. **Chosen:** *"Deep ensembles outperform snapshot ensembles and weight
   averaging for calibrated uncertainty under fixed training budgets"* —
   keeps the standard method names for findability, adds the scope qualifier
   demanded by the evidence, drops the coined "budget-split" label (which the
   text defines on first use).

## Numerical integrity checks performed on the v3 manuscript

- All v2-era numbers re-verified unchanged against `analysis_v2.json`
  (100+ values; script `verify_claims_v3.py`).
- Every CIFAR number in the v3 manuscript inserted programmatically from
  `analysis_cifar.json` (fill script; no manual transcription).
- Abstract length 250 words (IJMLC limit 150–250; guidelines re-checked
  2026-10-12). Keywords: 6.
- Compile: 0 LaTeX errors; overfull-hbox list re-checked after the CIFAR
  table fill.
