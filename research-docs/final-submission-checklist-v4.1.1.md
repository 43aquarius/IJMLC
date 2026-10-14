# Final Submission Checklist v4.1.1

**Journal:** International Journal of Machine Learning and Cybernetics (IJMLC)
**Guidelines source:** https://link.springer.com/journal/13042/submission-guidelines
**Guidelines access date:** 14 October 2026 (recorded as required)
**Manuscript:** `deep-ensembles-fixed-budget-paper-v4.1.1.pdf` (25 pp., A4)

Legend: PASS = verified this session on the compiled artefacts;
AUTHOR = requires the author's information or action; N/A = not applicable.

## A. Official requirements vs manuscript state

| # | Official requirement (as read on 14 Oct 2026) | Manuscript state | Result |
|---|---|---|---|
| A1 | Abstract 150–250 words; no undefined abbreviations or unspecified references | 236–238 words (three counting rules recorded); NLL/OOD defined at first use; no citations in abstract | PASS |
| A2 | 4–6 keywords | 6 keywords | PASS |
| A3 | Statements under the heading "Statements and Declarations"; submissions without relevant declarations returned as incomplete | Heading used; six standard paragraphs (Funding / Competing interests / Author contributions / Use of large language models / Data availability / Code availability) | PASS |
| A4 | Author Contribution and Competing Interest info must also be provided via the submission interface (only interface entries appear in the published version) | Present in manuscript; **author must re-enter the same text in the submission system** | AUTHOR |
| A5 | Competing-interests disclosure (blanket statement acceptable when there are no interests) | Single-author no-conflict statement | PASS |
| A6 | Funding sources written in full, or no-funding statement | Springer standard no-grant statement inserted | AUTHOR — **confirm it matches reality** |
| A7 | Research Data Policy: data availability statement required for original research | Data availability paragraph names all datasets with citations and points to the public repository | PASS |
| A8 | LLMs do not satisfy authorship criteria; LLM use documented in Methods; AI-assisted copy editing alone need not be declared; human accountability | Methods paragraph + full Statements-and-Declarations disclosure; AI involvement in code/analyses/figures/draft/revisions disclosed (beyond copy editing, so it is declared in both places) | PASS |
| A9 | Generative AI images must follow Springer's policy | All figures are deterministic matplotlib renders of experimental data; no generative-AI imagery used | PASS (N/A for gen-AI images) |
| A10 | LaTeX accepted ("Manuscripts with mathematical content can also be submitted in LaTeX"; Springer template recommended, not mandated) | Compilable single-file LaTeX source with standard packages | PASS (template conversion optional, not done near submission — see D2) |
| A11 | Editable source files must be provided at submission | `main_v4_1_1.tex` + figure PDFs + `.bib`-equivalent inline bibliography | PASS |
| A12 | Title page: title, author, affiliation, corresponding-author e-mail, ORCID if available | Title, author, affiliation, e-mail present; **ORCID absent — add if you have one (optional)** | AUTHOR (optional) |
| A13 | Decimal headings, ≤3 levels | Sections/subsubsections comply | PASS |
| A14 | Abbreviations defined at first mention | Verified for NLL, ECE, OOD, AUROC, TS, SWA, DeepEns, Snapshot, Single | PASS |
| A15 | Acknowledgments on a separate title page | None present (no acknowledgments to make) | N/A |

## B. Internal consistency (verified this session)

| # | Check | Result |
|---|---|---|
| B1 | Bibliography byte-identical v4.1.0 → v4.1.1 (no entry added/removed/edited) | PASS |
| B2 | Citation two-way check: 28 bib keys, 28 cited; none uncited, none missing | PASS |
| B3 | Cross-references: 37 labels / 23 refs, zero unresolved; 0 `??` in PDF | PASS |
| B4 | 9 `includegraphics` (5 main + 4 supplementary) all resolve and render | PASS |
| B5 | VLM legibility pass on all 9 figures (pages 20–24) | PASS (Fig. 3 note: one annotation "tight but readable" — acceptable; no action required) |
| B6 | Supplementary Figure S3 x-labels (the Fig. 8 crowding problem) | FIXED — VLM: "clearly readable without overlap or clipping" |
| B7 | Figure S3 data integrity: plotted seed values identical to `figure_data.json` | PASS (programmatic assertion) |
| B8 | Compile: 0 errors, 0 overfull/underfull boxes, 3-pass cross-reference convergence | PASS (tectonic 0.15.0 log kept) |
| B9 | No old-version leftovers in PDF (`Declarations` heading, `paper-v4.0.0` tag, old paragraph names) | PASS |
| B10 | Claims guardrails re-checked after editing (ECE-CIFAR unresolved; MNIST boundary; OOD evidence tiers; associational mechanism; TS not rank-preserving; budget vs inference cost; pre-reg vs post-hoc labels) | PASS — no regression |
| B11 | v4.1.0 audit exceptions (9/241) all carry documented dispositions | PASS (read and confirmed; none affects manuscript numbers) |
| B12 | Cover letter exists and matches v4.1.1 claims | PASS (draft created; author to finalise) |

## C. Files produced this session

- `manuscript-source/main_v4_1_1.tex` — revised source
- `figures/suppl_fig3_swa_dense.pdf` / `.png` — regenerated at 7.2 in width
- `paper/deep-ensembles-fixed-budget-paper-v4.1.1.pdf` — to be attached to the release upon author authorisation
- `research-docs/revision-log-v4.1.1.md` (this directory), `research-docs/final-submission-checklist-v4.1.1.md`, `research-docs/cover-letter-v4.1.1.md`
- Local git branch with a single v4.1.1 commit (not pushed; no tag created; no release published)

## D. Remaining actions before submission (author)

1. **[Required]** Confirm or correct the Funding statement (A6) and, if funding
   exists, name the source in full.
2. **[Required]** Enter Author Contributions and Competing Interests in the
   journal submission interface (A4); consider adding ORCID (A12).
3. **[Required upon authorisation]** Push the v4.1.1 branch, tag
   `paper-v4.1.1`, and attach the PDF as the release asset (this session was
   explicitly not authorised to publish).
4. **[Optional]** Springer Nature LaTeX template conversion (D2/A10): the
   guidelines recommend but do not mandate it; recommended to skip for this
   submission cycle to avoid late-stage churn.
5. **[Optional, future work]** The two optional experiments from the v4.1
   assessment (BN-replication; CIFAR-10-C corruptions) remain future work and
   do not block submission.
