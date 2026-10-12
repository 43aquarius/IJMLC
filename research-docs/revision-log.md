# Revision Log: v1 → v2 (Deliverable E)

Mapping of every audit issue (see audit-report.md) to the fix applied in the v2 manuscript,
its evidence, and whether new experiments were required. "v2 location" refers to the IJMLC-format
manuscript `main_v2.tex`.

| ID | Priority | v1 problem | v2 fix | v2 location | Evidence | New experiment |
|----|----------|-----------|--------|-------------|----------|----------------|
| A-01 | P0 | Text cites [19]; bibliography ends at [18] | Author-year citations via natbib; numbering eliminated | whole manuscript | 0 unresolved refs in compiled PDF | No |
| A-02 | P0 | Dataset citations off by one | (LeCun et al. 1998) / (Xiao et al. 2017) bound correctly | §3.2 | grep check | No |
| A-03 | P0 | Snapshot-ensemble sentence cited "easily fooled" | Correct binding to (Loshchilov and Hutter 2017) | §1 ¶1 | manual check | No |
| A-04 | P0 | UQ sentence cited Fashion-MNIST dataset paper | Correct binding to (Abdar et al. 2021; Ovadia et al. 2019) | §1 ¶1 | manual check | No |
| A-05 | P0 | Author block missing/pending | Chang Tan, Dalian University of Technology, corresponding author aquars43@foxmail.com; sole author | title block | user-provided | No |
| A-06 | P0 | No AI disclosure; workflow branding on title page | Declarations: AI-use disclosure (factual wording); branding text removed from title block; workflow named only in the disclosure | Declarations | manual | No |
| A-07 | P1 | One dataset family | MNIST-ID direction added (10 replicates) + boundary-condition finding | §4.2, Fig. 4a, Table 3 | experiment_v2_mnist_B60_k3.jsonl | **Yes** |
| A-08 | P1 | One shift type | KMNIST second probe in all settings | §3.2, §4.4, Fig. 4b | all v2 JSONLs | **Yes** |
| A-09 | P1 | No post-hoc recalibration baseline | Per-condition temperature scaling fitted on validation | §3.4, §4.3, Fig. 3, Table S3 | all v2 JSONLs ('ts' blocks) | **Yes** |
| A-10 | P1 | One budget | B=30 and B=120 settings (10 replicates each) | §4.2, Fig. 2a, Table 3 | experiment_v2_fmnist_B{30,120}_k3.jsonl | **Yes** |
| A-11 | P1 | One ensemble size | k=5 setting (10 replicates) | §4.2, Fig. 2b, Table 3 | experiment_v2_fmnist_B60_k5.jsonl | **Yes** |
| A-12 | P1 | Nature-style formatting | IJMLC conventions: author-year, alphabetical references, separate Related Work (§2), conventional IMRaD, 150–250-word abstract (239 words), 6 keywords | whole manuscript | pdf_qa | No |
| A-13 | P2 | "13 minutes per seed" factually wrong | Corrected: 72–87 s per B=60 replicate; 9,000 extension epochs / 69 min; ~11,200 epochs total | §3.3 | JSONL wallclock_s | No |
| A-14 | P2 | Abbreviated journal names | Springer-style full forms (e.g., "Information Fusion", "Proceedings of the IEEE") | references | manual | No |
| A-15 | P2 | No repository URL | github.com/43aquarius/IJMLC cited; release paper-v2.0.0 | Declarations | repo live | No |
| A-16 | P2 | Abstract 249 words, no keywords | Rewritten 239-word abstract; 6 keywords | abstract | word count check | No |
| A-17 | P2 | MLP-only architecture | Honestly stated in Limitations; offered as direct future work | §5.1 | — | Would need GPU |
| A-18 | P3 | Stale date | 11 October 2026 | title block | — | No |
| A-19 | P3 | Fig 1 caption details | Caption updated (still accurate; data unchanged and re-verified) | Fig. 1 | VLM check | No |
| A-20 | P3 | Repo README placeholder author | README updated: Chang Tan; v2 results; new figure list | repo README | repo | No |

## Additional v1→v2 content changes (beyond the audit items)

1. **New findings integrated:** budget-sweep growth of the budget-split advantage (§4.2);
   MNIST saturation boundary condition (§4.2); TS compresses-but-does-not-close result (§4.3);
   OOD generality across 4 probe–direction combinations (§4.4); k=5 mechanism nuance (§4.5).
2. **New figures:** Fig. 2 (budget & size), Fig. 3 (temperature scaling), Fig. 4 (direction &
   OOD overview) — each with per-panel CSV source data; all VLM-checked.
3. **New supplementary table:** Table S3 (TS-NLL contrasts across all settings).
4. **Discussion rewritten** around the five-way evidence; practical guidance now includes
   the TS recommendation ("apply temperature scaling regardless: it is nearly free …").
5. **Claim–evidence map updated** for all new claims (see claim-evidence-map-v2.md).

## Numerical integrity checks performed on the v2 manuscript

- Every contrast value, CI and p-value in Tables 1–3 and S1–S3 diffed against
  `results/v2/analysis_v2.json` (and v1 `analysis.json` for the core setting).
- Abstract numbers (0.289/0.333, −0.016, P≥0.41, P=0.0098) match the analysis outputs.
- E-A raw metrics equal v1 values bit-for-bit (28/28 on seed 0; full-file equality of
  condition means for all seeds).
- Compute-exactness formula corrected (2B + (k−1)B/k, verified against the training script).
