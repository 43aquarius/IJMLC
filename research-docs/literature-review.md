# Literature Review & Verification Report (Deliverable B)

**Session:** 11 October 2026 · **Manuscript:** budget-split ensembles (v2, IJMLC target)
**Method:** live web search (z-ai web_search) per reference; v1 references were verified in the
original session and re-spot-checked here. Every reference below was confirmed to exist with the
listed first author, year and venue. References whose full author list could not be re-verified
online are cited in the manuscript in the honest "et al." form rather than with a guessed list.

---

## 1. Verified reference inventory (21 entries in v2)

| # | Key | Status | Verification notes |
|---|-----|--------|--------------------|
| 1 | abdar2021, Inf. Fusion 76:243–297 | kept (v1-verified) | Review of UQ in DL |
| 2 | ashukha2020, ICLR | kept (re-verified) | arXiv:2002.06470, ~508 citations; closest prior budget-matched work |
| 3 | clanuwat2018, NeurIPS workshop | **ADDED** | KMNIST source; full author list verified (Clanuwat, Bober-Irizar, Kitamoto, Lamb, Yamamoto, Ha); arXiv:1812.01718 |
| 4 | fort2019, arXiv:1912.02757 | kept (v1-verified) | Title verified in v1 ("Deep Ensembles: A Loss Landscape Perspective") |
| 5 | gal2016, ICML | kept (v1-verified) | MC dropout |
| 6 | guo2017, ICML | kept (v1-verified) | Calibration + temperature scaling |
| 7 | hendrycks2017, ICLR | kept (v1-verified) | MSP baseline |
| 8 | huang2017, ICLR | kept (v1-verified) | Snapshot ensembles |
| 9 | izmailov2018, UAI | kept (v1-verified) | SWA |
| 10 | lakshminarayanan2017, NeurIPS 30 | kept (v1-verified) | Deep ensembles |
| 11 | lecun1998, Proc. IEEE 86(11) | kept (v1-verified) | MNIST |
| 12 | loshchilov2017, ICLR | kept (v1-verified) | SGDR cosine restarts |
| 13 | maddox2019, NeurIPS 32 | kept (v1-verified) | SWAG |
| 14 | naeini2015, AAAI | kept (v1-verified) | ECE binning |
| 15 | nguyen2015, CVPR | kept (v1-verified) | Easily fooled |
| 16 | ovadia2019, NeurIPS 32 | kept (v1-verified) | First author + venue confirmed again |
| 17 | welling2011, ICML | kept (v1-verified) | SGLD |
| 18 | wen2020, arXiv:2002.06715 | **ADDED** | BatchEnsemble; arXiv id confirmed; cited as arXiv preprint (venue not asserted) |
| 19 | wilson2020, NeurIPS 33 | kept (v1-verified) | Bayesian DL |
| 20 | xiao2017, arXiv:1708.07747 | kept (v1-verified) | Fashion-MNIST |
| 21 | zhang2020, AISTATS (PMLR) | **ADDED** | Mix-n-Match; PMLR proceedings + ~382 citations confirmed; "et al." author form |

**Removed from consideration:** Havasi et al. (MIMO) — paper exists but full bibliographic
details (exact title/author order/venue) could not be verified reliably via search; the
single-network-ensemble family is already represented by BatchEnsemble. Schweighofer et al.
2024 (arXiv:2410.13831, "The Disparate Benefits of Deep Ensembles") — verified to exist but
tangential (fairness angle); omitted to keep the reference list tight. No IJMLC-specific article
on our topic could be verified with full bibliographic details, so none is cited (fabricating a
journal-fit citation is not an option).

## 2. v1 citation defects and their repair (audit items A-01…A-04)

The v1 manuscript hard-coded numeric superscript citations. Four defects were found:
(i) the text cited [19] while the bibliography ended at [18]; (ii) the Fashion-MNIST and MNIST
dataset citations were shifted by one position; (iii) the snapshot-ensemble sentence cited
Nguyen et al. "easily fooled" instead of the SGDR paper; (iv) a UQ body-of-work sentence cited
the Fashion-MNIST dataset paper. **Repair:** the v2 manuscript uses `natbib` author–year
citations throughout (`\citep`/`\citet`), which eliminates the numbering-drift failure mode
entirely; the bibliography is alphabetically ordered by first author surname per IJMLC style.
Every in-text citation was re-bound to the correct reference during the rewrite.

## 3. Novelty check (is the budget-matched comparison already published?)

Searches for budget/compute-matched comparisons of deep ensembles, snapshot ensembles and
SWA returned: (a) Ashukha et al. 2020 — compute-matched single-vs-ensemble analyses exist,
but no snapshot-ensemble or checkpoint-matched SWA contrast; (b) Ovadia et al. 2019 —
multi-method shift benchmark, budgets not matched; (c) efficient-ensemble literature
(BatchEnsemble etc.) — reduces member cost, a different axis from allocating a fixed budget;
(d) calibration-ensemble interaction literature (Mix-n-Match; recent "joint regularization
and calibration in deep ensembles" work) — studies post-hoc calibration and ensembling
together but not budget allocation. **Conclusion:** the specific four-way, checkpoint-matched,
seed-paired design with per-condition temperature scaling appears novel as a *comparison
design*; no claim of algorithmic novelty is made. This positioning is stated explicitly in
Sect. 2 (Related work, "Positioning" paragraph) of the v2 manuscript.

## 4. Innovation matrix (v2 findings vs. closest prior work)

| Finding | Closest prior support | What v2 adds |
|---|---|---|
| Ensembles > single for NLL/calibration | Lakshminarayanan 2017; Ashukha 2020 | Same-budget, same-checkpoint allocation; 5 settings; exact permutation inference |
| DeepEns > Snapshot at matched budget | (not isolated before) | Clean contrast via shared first member; mechanism (member NLL 0.338 vs 0.404; JSD 0.0150 vs 0.0106) |
| Snapshot > SWA on same checkpoints | (not isolated before) | Identical-checkpoint function-space vs parameter-space contrast |
| Prediction averaging improves OOD, weight averaging does not | Ovadia 2019 (methods differ in budget) | Checkpoint-matched isolation; 4 probe–direction combinations |
| TS improves single models but ensembles stay ahead | Guo 2017; Lakshminarayanan 2017 | Budget-matched replication with per-condition TS; OOD invariance of TS |
| Longer training worsens calibration | Guo 2017 (implicitly) | Quantified as the driver of the growing budget-split advantage (B=30→120) |
| Ensemble gains vanish on saturated tasks | (scattered observations) | Controlled MNIST-direction boundary condition with significance tests |

## 5. Search-engine limitations (recorded for transparency)

Two classes of query returned irrelevant results (searches for "budget-matched comparison…"
and some author-list queries returned dictionary/failure results). All references central to
the paper's claims were nevertheless verified through at least one targeted query, and
unverifiable details were avoided in the final reference list (see "et al." policy above).
Raw search results are preserved in `tool-results/litsearch/` of the working directory and
summarised here.
