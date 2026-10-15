# Revision Log v4.1.2 (submission-package finalisation)

**Base:** `paper-v4.1.1` (commit a532181, release PDF SHA-256
`72fe01b1...` per the canonical-URL rebuild record)
**New version:** v4.1.2 · **Date:** 15 October 2026
**Scope:** submission-package finalisation only. No experiment was added,
re-run or modified; no reported number, table, figure, statistic or
bibliography entry was changed; no historical version, tag or release was
overwritten. The v4.1.0 numeric audit (232/241 checks, 9 documented
dispositions) remains the authority for all reported numbers.

## Summary of edits (all verified on the compiled PDF)

| # | Location | Change in v4.1.2 | Verification |
|---|---|---|---|
| 1 | Methods §3.6 (Reproducibility), final paragraph | The `Use of large language models` paragraph was removed at the author's decision for the submission version | Word-multiset diff of extracted PDF text: removals are exactly the two LLM paragraphs, their two headings, the date token and one page number; nothing else changed |
| 2 | Statements and Declarations | The `Use of large language models` paragraph was removed at the author's decision; the section now carries five paragraphs (Funding / Competing interests / Author contributions / Data availability / Code availability) | PDF text extraction confirms all five headings; no residual "language model"/"LLM" text anywhere in the PDF |
| 3 | Title page date | 14 October 2026 → 15 October 2026 | PDF text; the single remaining "14 October 2026" is the literature-search date in the positioning statement (§2), which is correct and retained |
| 4 | Page count | 25 pp. → 24 pp. (consequence of the two removed paragraphs) | pdfinfo; A4; 0 compile errors; 0 overfull boxes; no undefined citations/references (the only log "undefined" is a benign TU/lmr/bx/sc font-shape substitution, unchanged from earlier versions) |

## Explicitly NOT changed

- Every reported number, table, statistic and their wording. Red-line
  spot checks passed on the compiled PDF: CIFAR-10 ECE "not statistically
  resolved"; MNIST near-saturation boundary; OOD tiers with SWA "small,
  task-dependent"; anomalous-seed passage (NLL 0.929 / ECE 0.210)
  retained verbatim; temperature-scaling hedges; pre-registered vs
  post-hoc labels.
- The bibliography: entries identical between v4.1.1 and v4.1.2
  (extracted references sections differ only in the position of one
  page-number token caused by the page break shifting).
- All figures (identical files re-embedded; Figure S3 remains the widened
  7.2-inch version from v4.1.1).
- The repository URL (canonical name) in §3.6 and Code availability, at
  submission-package build time. The Code-availability release pointer was
  subsequently updated from `paper-v4.1.1` to `paper-v4.1.2` when the
  author authorised publishing this release — see the appendix below for
  the verification of that token-only change.
- All raw data, per-replicate records and analysis outputs.

## Submission-package files produced alongside this revision

- `submission/cover-letter-Chang-Tan.docx` / `.pdf` — one-page cover
  letter (research question; design; findings with their stated limits;
  not-a-new-algorithm positioning; journal fit; originality, sole
  author, no funding, no competing interests, data/code availability).
  Metadata: author "Chang Tan".
- `submission/author-contributions-statement-Chang-Tan.docx` / `.pdf` —
  one-page statement using initials (C.T.), mirroring the manuscript's
  Author-contributions paragraph; prepared for the submission-system
  field that replaces any in-manuscript statement.
- `deep-ensembles-fixed-budget-manuscript-source-v4.1.2.zip` —
  manuscript-source/main_v4_1_2.tex + the 9 figure PDFs + BUILD.txt
  (the editable LaTeX upload per the journal interface).

## Notes for the author (not part of the submission)

- The IJMLC submission interface accepts the manuscript either as a
  Word document with figures in the body, or as a zipped LaTeX source;
  the LaTeX zip is the editable format of record here, and the journal
  compiles it for peer review.
- The public repository release `paper-v4.1.2` has been published at the
  author's authorisation (15 October 2026) with the submission PDF and
  source zip as assets — see the appendix below.

## Appendix: release publication (15 October 2026)

The author authorised publishing the `paper-v4.1.2` release
("需要，发布到release", this session). Actions taken:

- **A1. Release-pointer update.** The Code-availability release pointer in
  `main_v4_1_2.tex` (single occurrence, p. 16 area) was updated from
  `paper-v4.1.1` to `paper-v4.1.2`, following the repository's per-version
  convention (each version's PDF names its own release tag).
- **A2. Recompile and verification.** Tectonic 0.15.0 recompile: 0 errors,
  0 Overfull boxes, no undefined citations/references (only the benign
  TU/lmr/bx/sc font-shape substitution present in all previous versions);
  24 pages, A4; PDF metadata unchanged (Title "Deep ensembles ...",
  Author "Chang Tan"). A reverse-substitution proof (scripts/
  `verify_v412_release.py`) shows that replacing the new tag token
  `paper-v4.1.2` back to `paper-v4.1.1` in the extracted PDF text restores
  the previously compiled v4.1.2 PDF's text **character-for-character** —
  the rebuild is a token-only change. All 39 submission checks pass on the
  rebuilt PDF (declarations, red-line numbers and hedges, dates, page
  count, log checks, metadata).
- **A3. Word-level diff.** The pairwise word-multiset difference between
  the pre-update and rebuilt v4.1.2 PDFs is exactly
  `{'paper-v4.1.1).' : 1}` removed and `{'paper-v4.1.2).' : 1}` added.
- **A4. References note.** The v4.1.1 → v4.1.2 references-section
  difference recorded above (one page-number token moved by the page
  break) is pre-existing and unchanged by the rebuild; pre-update and
  rebuilt v4.1.2 references sections are byte-identical. `verify_v412.py`
  was updated to compare references modulo standalone page-number
  tokens and to expect the `paper-v4.1.2` pointer; both verification
  scripts pass on the released artefacts.
- **A5. Source zip rebuilt and clean-room recompiled.** The manuscript
  source zip was rebuilt with the updated tex; a clean-directory
  extraction and tectonic recompile reproduces the canonical PDF text
  exactly (24 pages, pointer present).
- **A6. Release assets.**
  - `deep-ensembles-fixed-budget-paper-v4.1.2.pdf` — 384,860 bytes,
    SHA-256 `40321b244b7d70b6b5cd3420574c34a43c8070263a8bb13859bdd870a4654b72`
  - `deep-ensembles-fixed-budget-manuscript-source-v4.1.2.zip` —
    221,888 bytes,
    SHA-256 `487eefcd30396b6af2fcd3ef930f8556cd65f8bdbaf05a64b67d346695f791c3`

  Release URL:
  https://github.com/43aquarius/deep-ensembles-fixed-budget/releases/tag/paper-v4.1.2
  Asset digests are verified server-side after upload (GitHub API
  `digest` field). The `download/ijmlc-submission-package-v4.1.2/`
  manuscript copies were refreshed to the rebuilt PDF and zip, so the
  submission package and the public release are byte-identical.
- **A7. Untouched.** No earlier tag, release or asset was modified; the
  repository tree continues to carry supporting materials only (the
  manuscript PDF and LaTeX source live exclusively in the release
  assets).
