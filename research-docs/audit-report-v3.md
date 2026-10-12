# Research Audit Report v3 (Deliverable A)

**Manuscript:** "Budget-split deep ensembles outperform snapshot ensembles and weight
averaging for calibrated uncertainty" — v2 (19 pp., 11 Oct 2026)
**Target journal:** International Journal of Machine Learning and Cybernetics (IJMLC)
**Audit date:** 12 October 2026 (session 3)
**Auditor roles:** ML researcher / IJMLC reviewer / literature researcher / statistics
auditor / Python-PyTorch engineer / English editor

---

## 1. Verification work performed this round (evidence base)

1. **Full re-read of the 19-page v2 manuscript** against the raw result files.
2. **Numerical re-verification (script: `scripts/verify_claims_v3.py`):** 100+ reported
   values (Tables 1–3, S1–S3, abstract, results text) diffed against
   `results/v2/analysis_v2.json` — **all PASS** at rounding tolerance (≤6e-4).
   This includes every contrast estimate, CI bound, permutation P, Holm P, condition
   mean/s.d., fitted temperatures, and mechanism measurements (member NLL, JSD).
3. **Independent recomputation of the exact sign-flip permutation tests:** all
   per-seed deltas re-enumerated (all 2^10 sign patterns) in the audit script —
   **every p_perm_exact in analysis_v2.json reproduced exactly**. The statistical
   machinery is internally consistent and independently verifiable.
4. **"AI-generated" watermark investigation (user-reported, page 19 bottom-right):**
   (i) text-layer extraction of all 19 pages — no such string; (ii) raw PDF content
   streams scanned — no "AI"/"生成"/"Generated"/"watermark" operators on any page;
   (iii) 110-dpi full-page and 200-dpi bottom-right-corner renders inspected by a
   vision model — clean; (iv) the GitHub Release asset is byte-identical to the
   local build (MD5 `cdc5692456b2da760200f44d740ba31d` both). **Conclusion: the
   watermark is not in the manuscript file; it is added by a viewing/downloading
   application (e.g., office/file-preview tools that stamp AI-originated files).
   The official manuscript and release PDF are clean.** Action for the author: view
   the PDF in a plain viewer (browser/Acrobat) before submission; nothing to remove
   in the source.
5. **Compute-fairness re-audit (code-level):** `run_experiments_v2.py`/`common.py`
   reviewed line-by-line. All four conditions consume identical optimizer update
   counts (211 steps/epoch × B epochs on the shared 54k split; DeepEns = k × (B/k)
   epochs). Identical optimizer family, weight decay, batch size, LR ceiling and
   per-step cosine implementation. First ensemble member of DeepEns and first
   snapshot are the same bit-identical network (verified `shared_member_bit_identical:
   true` in every setting's analysis record). **The training-budget match is exact;
   inference cost is NOT matched (see V3-05).**
6. **Temperature-scaling implementation audit:** single models and ensembles both fit
   T on the effective logit vector z = log p via validation-NLL minimisation
   (grid + golden-section). For single networks, softmax(log p / T) = softmax(z/T)
   exactly (softmax shift invariance), so the Methods statement of equivalence to
   standard Guo-style temperature scaling is correct. For ensembles this is the
   standard log-mean-prob extension; the paper correctly avoids calling it the only
   possible ensemble calibration.
7. **OOD orientation audit:** MSP with in-distribution as positive class; negative-
   entropy score s = Σ p·log p (higher = more ID-like) — orientation correct in all
   probes and both directions; consistent definitions across settings.

---

## 2. v3 issue register (unresolved issues in the v2 manuscript)

Priorities: **P0** = blocking correctness/compliance · **P1** = likely reviewer
rejection vector · **P2** = weakens paper · **P3** = polish.
"Fixed in v3" column refers to the revision produced in this session.

| ID | Pri | Location (v2) | Issue | Evidence (from raw data) | Impact | Fix | New experiment? | Fixed in v3 |
|----|-----|---------------|-------|--------------------------|--------|-----|-----------------|-------------|
| V3-01 | **P1** | Abstract: "the ordering DeepEns > Snapshot > SWA > Single on every in-distribution metric … The ordering was robust across budgets (30, 60, 120), ensemble sizes and a reversed dataset direction" | Over-generalisation. The every-metric ordering holds at B=60 (core) and B=120 only. At B=30: accuracy ordering is Snapshot (0.8929) > Single (0.8917) > SWA (0.8914) > DeepEns (0.8905); DeepEns−Single accuracy = −0.0012 [−0.0021,−0.0002] (p=0.018 uncorrected), DeepEns−Snapshot accuracy = −0.0025 [−0.0040,−0.0010] (p=0.002). Brier at B=30: Snapshot 0.1562 < DeepEns 0.1573. At k=5: accuracy Snapshot 0.8944 > DeepEns 0.8938. | `analysis_v2.json` fmnist_B30_k3, fmnist_B60_k5 | Reviewer finding one counterexample (they are in our own released data) would taint every other claim | Abstract and §4.2 rewritten: the **NLL and ECE** ordering is robust across all five Fashion-MNIST settings; secondary metrics show bounded exceptions (≤0.003) at B=30 and k=5, stated explicitly with numbers | No (data exist) | Yes |
| V3-02 | **P1** | §4.3: "The same two conclusions held in every extension setting: after TS, DeepEns remained significantly better than Single on NLL at B=30 (−0.0114)…" | Misleading by scope: at B=30 after TS the *ensemble ordering inverts*: TS-NLL Snapshot 0.2986 < DeepEns 0.3013 < SWA 0.3040 < Single 0.3126, and DeepEns−Snapshot on TS-NLL = **+0.0026 [+0.0002,+0.0050], p_holm=0.0449** (Snapshot significantly better). "DeepEns vs Single significant everywhere" is true; "the ordering persisted" is not true at B=30 post-TS. | `analysis_v2.json` fmnist_B30_k3 ts.nll contrasts | Direct contradiction between text and released data; a P0-grade credibility risk if noticed | §4.3 rewritten: DeepEns vs Single robust everywhere, but at B=30 post-TS the ensembles are statistically indistinguishable-to-inverted (Snapshot nominally best); strengthens the honest "TS is a genuine partial substitute at small budget" point already present | No (data exist) | Yes |
| V3-03 | **P1** | Whole paper | No cross-architecture evidence; single model family (MLP), grayscale 28×28 only | — | The #1 rejection vector for any empirical ML paper; v2 defers it to Limitations | **CIFAR-10 + SmallCNN (34k params, 3 conv blocks) extension designed, executed this session** (B=60, k=3, 10 seeds, identical protocol; post-hoc-labelled) | **Yes** | Yes (executed) |
| V3-04 | **P1** | Title | "…outperform … for calibrated uncertainty" — scope broader than evidence; no budget qualifier | Title review (§10.1 of directive) | Reviewers may read "outperform" as a general claim; the evidence is fixed-budget, small-network | Title rescoped: **"Deep ensembles outperform snapshot ensembles and weight averaging for calibrated uncertainty under fixed training budgets"** (candidates compared in the revision log) | No | Yes |
| V3-05 | **P2** | Methods/Discussion | Training budget matched, but **inference cost** (k forward passes for either prediction-averaging ensemble vs 1 for Single/SWA) never stated explicitly; the four cost dimensions (training budget / wall-clock / inference / deployment) are not separated | §3.1, §5 | Conflation of "budget-matched training" with "matched deployment cost" — exactly the failure mode the integrity rules prohibit | New paragraph in Methods (§3.1) + one sentence in Discussion; practical guidance updated | No | Yes |
| V3-06 | **P2** | §4.2 sentence | "The ensemble effect that longer training damages calibration and averaging repairs it---requires headroom that the near-saturated MNIST task does not provide" — garbled punctuation/logic; also "requires" reads causal | text review | Readability; causal overtones on an associational finding | Rewritten: "The ensemble effect documented here—longer training damages calibration and averaging repairs it—is observed only where such damage exists; the near-saturated MNIST task provides no such headroom" (associational wording) | No | Yes |
| V3-07 | **P2** | §4.4 OOD | MNIST-direction OOD P values (+0.0139, P=0.008; +0.0235, P=0.002) not explicitly labelled uncorrected/descriptive in that sentence (the core-setting SWA/KMNIST case IS labelled) | `analysis_v2.json` (OOD = secondary family, uncorrected) | Inconsistency in multiplicity labelling | Sentence amended: "(uncorrected exact P; OOD contrasts are secondary)" | No | Yes |
| V3-08 | **P2** | §5 Discussion | "which include most practically deployed under-trained or heavily optimised classifiers" — claim about deployment reality with no citation or survey | §5 ¶3 | Uncited external claim; reviewer objection | Reworded to an explicitly hedged statement tied to the measured overconfidence mechanism (no deployment survey claimed) | No | Yes |
| V3-09 | **P2** | §4.4 / Abstract | "SWA showed no reliable improvement" (OOD) — at core-setting KMNIST the uncorrected P is 0.023 with Δ=+0.0112; text explains this, but the abstract phrase "no reliable improvement" could be read as "proved null" | `analysis_v2.json` core auroc_msp_kmnist | Nuance needed to honour "no non-significant ⇒ equivalent" rule | Abstract and §4.4 wording: "no improvement that survives correction for multiplicity (largest uncorrected effect +0.011, P=0.023, an order of magnitude smaller than either prediction-averaging strategy)"; §4.4 already contains the absence-of-evidence caveat — kept and tightened | No | Yes |
| V3-10 | **P3** | References | `\begin{thebibliography}{22}` but 21 entries | source check | Cosmetic | Fixed to {21}; reference list re-alphabetised after additions | No | Yes |
| V3-11 | **P3** | Related Work | 2024–2026 coverage thin: Ajroldi et al. (ICML 2025) weight-averaging benchmark; Chirkova et al. (2020) fixed-**memory**-budget ensembles; Thuy & Benoit (2024) applied cheaper-ensemble study not cited | literature re-check (this session, Section 3 below) | Reviewers check recent work; missing the closest 2025 paper on weight averaging is a visible gap | Three verified references added with positioning sentences; novelty claim re-checked (still uncovered: checkpoint-matched prediction-vs-weight averaging with calibration/OOD) | No | Yes |
| V3-12 | **P3** | §3.3 | "Enlarging the ensemble from k=3 to k=5 … improved every strategy" — Single is unchanged by k (bit-identical runs; NLL 0.52649 both), so "every strategy" could mislead if read to include Single | `analysis_v2.json` single nll equal across k3/k5 settings | Minor precision | Reworded: "improved every ensemble strategy (Single is unchanged by construction)" | No | Yes |

**Resolved in v2 and re-confirmed this round (not re-opened):** citation-numbering
defects A-01..A-04 (author-year system eliminates the failure mode), author block
(Chang Tan, DUT, sole & corresponding), AI-use disclosure in Declarations, IJMLC
structure (author-year, alphabetical refs, 239-word abstract, 6 keywords),
timing corrections (72–87 s/replicate), repository + release linkage.

---

## 3. Literature re-check (2024–2026) — summary

Full details in `literature-review-v3.md` (Deliverable B). Headline: the v2 novelty
statement survives the 2024–2026 re-check. Closest new works and their relationship:

- **Ajroldi, Orvieto, Geiping (ICML 2025): "When, Where and Why to Average Weights?"**
  Large-scale AlgoPerf benchmark of checkpoint averaging: accelerates training, mildly
  improves generalisation. No calibration, no OOD detection, no snapshot-ensemble
  contrast, no checkpoint-matched prediction-vs-weight comparison. → Cite; our
  contribution is complementary (uncertainty quality, not optimisation speed).
- **Chirkova, Lobacheva, Vetrov (2020, arXiv:2005.07292): "Deep ensembles on a fixed
  memory budget: one wide network or several thinner ones?"** Fixed-resource ensemble
  splitting for **memory**, not training compute; no calibration/OOD. → Cite as the
  memory-axis analogue of our question.
- **Thuy & Benoit (2024, arXiv; journal version in Ann. Oper. Res.): "Reliable
  uncertainty with cheaper neural network ensembles: a case study in industrial
  parts classification"** — single vs deep ensemble vs three *efficient* ensembles
  in an applied setting; budgets not training-compute-matched; no SWA/snapshot. →
  Cite as applied context supporting the practical relevance of the question.
- No 2024–2026 work found that runs the **four-way budget-matched comparison with
  shared checkpoints** or isolates **prediction averaging vs weight averaging on
  identical checkpoints for calibration and OOD**.

---

## 4. Statistical audit (v3 pass over the 12 checklist items)

| # | Item | Status | Note |
|---|------|--------|------|
| 1 | Seed pairing respected | PASS | within-seed paired deltas everywhere; verified in JSON |
| 2 | Experimental unit = seed | PASS | n=10 per condition per setting |
| 3 | Paired mean + 95% CI | PASS | t-interval, df=9 |
| 4 | Exact sign-flip permutation | PASS | **independently recomputed this round; all match** |
| 5 | Holm correction on primary family | PASS | 5 contrasts × NLL per setting; TS family separate |
| 6 | Primary vs secondary separated | PASS | NLL primary; OOD/acc/Brier/ECE secondary uncorrected |
| 7 | Core vs extension labelling | PASS | core pre-registered; B/k/direction/probes/TS labelled extensions |
| 8 | Exploratory labelled | PASS | SWA-dense flagged exploratory |
| 9 | Non-significance not read as equivalence | PARTIAL → FIXED (V3-09) | wording tightened in v3 |
| 10 | Text ↔ table ↔ figure consistency | PASS after V3-01/V3-02 fixes | numbers verified; the two over-statements fixed |
| 11 | Analysis script independently executable | PASS | analyze_v2.py runs standalone; cross-checked against audit script |
| 12 | No outcome-based selection | PASS | no metric/contrast switching; all 5 contrasts reported everywhere |

**CIFAR extension pre-specification:** hypotheses, design, statistics and fallback
written to `research-docs/experiment-plan-cifar.md` **before** any test-set
evaluation (post-hoc-labelled, per integrity rule 11).

---

## 5. Reproducibility audit (repository)

Issues found and fixed this session (details in the code-audit report, Deliverable D):

1. **Hard-coded absolute paths** in shared modules (`/home/z/my-project/results/data/…`)
   — replaced by repo-relative defaults + CLI/env overrides in the refactored
   `code/` tree.
2. **Environment reset between sessions wiped the Python environment** — torch
   2.14.0+cpu reinstalled (exact version) and the v2 reproduction gate re-verified
   (seed 0: 28/28 recorded metrics bit-identical) before the CIFAR extension ran.
3. README reproduction instructions rewritten for a clean clone (no author-local
   directories); deterministic data download scripts provided (MNIST-family via
   documented mirrors; CIFAR via HuggingFace parquet mirrors of the official
   releases with integrity checks: per-channel means 0.4914/0.4822/0.4465, class
   counts).
