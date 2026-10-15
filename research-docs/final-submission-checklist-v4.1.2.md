# Final Submission Checklist v4.1.2

**Journal:** International Journal of Machine Learning and Cybernetics (IJMLC)
**Submission guidelines:** https://www.springer.com/journal/13042/submission-guidelines
(guidelines accessed 14–15 October 2026; submission-interface requirements read from the journal's upload page)
**Manuscript:** `deep-ensembles-fixed-budget-paper-v4.1.2.pdf` (24 pp., A4)

Legend: PASS = verified on the compiled artefacts this session;
AUTHOR = requires the author's information or action; N/A = not applicable.

## A. Submission-interface upload slots → files to upload

| Interface slot | What to upload | Status |
|---|---|---|
| **Manuscript file** (editable, max 2 GB; "LaTeX documents with figures and tables compressed into a .zip format. We will compile these into a PDF for peer review.") | `manuscript/deep-ensembles-fixed-budget-manuscript-source-v4.1.2.zip` (contains `manuscript-source/main_v4_1_2.tex`, the 9 figure PDFs, `BUILD.txt`; single-file source with inline author-year bibliography — no external `.bib`/`.cls` needed) | READY (compiles with tectonic and pdfLaTeX; verified this session) |
| — reference copy of the compiled PDF (for your records; the system builds its own PDF for review) | `manuscript/deep-ensembles-fixed-budget-paper-v4.1.2.pdf` | READY |
| **Figures and tables** (optional at initial submission; "if your submission is accepted, you will need to provide the original high-resolution images ... as separate files") | Nothing to upload now. The 9 figure PDFs are vector, and are both inside the zip and in the repository `figures/` directory for the post-acceptance stage | N/A at this stage |
| **Supplementary material** (optional; "supporting material that you want to be published alongside your manuscript") | Nothing to upload separately: the supplementary figures (S1–S4) and supplementary tables are part of the manuscript PDF, after the References section, as delivered in previous versions | N/A (embedded) |
| **Related files** (optional; overlapping-authorship papers, validation reports, correspondence; "these files will not be published") | Nothing to upload | N/A |
| **Cover letter** ("briefly discuss the context and importance of the submitted work and why it is appropriate for the journal") | `cover-letter/cover-letter-Chang-Tan.docx` (upload; the .pdf is an identical reference copy) | READY — one page, metadata author "Chang Tan" |
| **Author Contributions Statement** ("Use initials to refer to each author's contribution ... This replaces any statement written within the manuscript and is the one that we will publish.") | `author-contributions/author-contributions-statement-Chang-Tan.docx` (upload; .pdf identical) | READY — one page, C.T. initials, mirrors the manuscript's Author-contributions paragraph |

## B. Official requirements vs manuscript state (v4.1.2)

| # | Requirement | State | Result |
|---|---|---|---|
| B1 | Abstract 150–250 words | 236–238 words (three counting rules recorded in v4.1.1; untouched in v4.1.2) | PASS |
| B2 | 4–6 keywords | 6 keywords | PASS |
| B3 | Statements under the heading "Statements and Declarations" | Heading used; five paragraphs (Funding / Competing interests / Author contributions / Data availability / Code availability) | PASS |
| B4 | Funding statement | Springer standard no-grant wording ("no specific grant from any funding agency...") — confirmed by the author as accurate (no funding) | PASS (author-confirmed) |
| B5 | Competing interests | Single-author no-conflict statement | PASS |
| B6 | Data availability for original research | Names all datasets with citations; points to the public repository | PASS |
| B7 | Code availability | Repository URL (canonical name) + release pointer | PASS |
| B8 | Author-contribution info also entered via the interface (the published version comes from the interface) | Statement file prepared; **author must paste/enter it in the submission system** | AUTHOR |
| B9 | Editable source files at submission | LaTeX zip (single file + figures) | PASS |
| B10 | Title page: title, author, affiliation, corresponding e-mail, ORCID if available | All present; ORCID absent | AUTHOR (optional) |
| B11 | Decimal headings ≤3 levels; abbreviations defined at first mention | Verified in v4.1.1; unchanged | PASS |

## C. Verification performed on v4.1.2 this session

1. Compile (tectonic 0.15.0): 0 errors; no Overfull boxes; no undefined
   citations or references (the only "undefined" in the log is the benign
   TU/lmr/bx/sc font-shape substitution present in all previous versions).
2. Page count 24, A4; PDF metadata Title/Author correct ("Deep ensembles
   ..."/"Chang Tan").
3. No "large language model"/"LLM" text anywhere in the compiled PDF.
4. Word-multiset diff of extracted text, v4.1.1 → v4.1.2: the only
   removed content is the two withdrawn declarations paragraphs, their
   headings, the date token and one page number; the only addition is
   the new date. References section content identical (one page-number
   token shifts position with the page break).
5. Red-line numbers and hedges intact: 0.0407 / 0.0826 / 0.0845 / 0.0008
   (CIFAR-10 ECE CI), 0.7046 / 0.6799 (OOD AUROC), 0.929 / 0.210 / 2.017
   (anomalous-seed passage retained verbatim), P=0.0098 / 0.0020
   (Holm-adjusted / exact permutation), "not statistically resolved",
   "near-saturated MNIST", "every probe and direction", "compressed but
   did not close".
6. Canonical repository URL appears exactly twice (§3.6 and Code
   availability); no old repository name anywhere.
7. Cover letter and contributions statement: one page each; docx
   postcheck 0 errors; metadata author "Chang Tan"; docx and pdf
   versions identical in content; the statement uses initials (C.T.)
   per the interface instruction and is consistent with the manuscript's
   Author-contributions paragraph.
8. Release publication (15 Oct 2026, author-authorised): the
   Code-availability release pointer in the source was updated
   `paper-v4.1.1` → `paper-v4.1.2` and the PDF recompiled — proven a
   token-only change by reverse-substitution character-exact comparison
   of the extracted text against the previously compiled v4.1.2 PDF;
   39/39 checks pass (same red-line numbers, hedges, declarations,
   24 pp. A4, 0 errors, 0 Overfull). The source zip was rebuilt and
   clean-room recompiled with identical text. The `paper-v4.1.2` release
   carries the submission PDF and source zip; asset digests verified
   server-side. The `download/ijmlc-submission-package-v4.1.2/`
   manuscript copies are the released (rebuilt) files.

## D. Remaining actions before submission (author)

1. **[Required]** Enter the Author Contributions text in the submission
   system (B8) — paste from `author-contributions-statement-Chang-Tan.docx`.
2. **[Required]** Verify the funding and competing-interests entries when
   the submission-system forms auto-extract or prompt for them (they
   should read: no funding; no competing interests; sole author).
3. **[Optional]** Add ORCID on the title page / profile (B10).
4. **[Resolved]** The public release decision (previous open item):
   `paper-v4.1.2` was published on 15 October 2026 at the author's
   authorisation, with the submission PDF and source zip as assets and
   the in-manuscript Code-availability pointer updated to `paper-v4.1.2`
   (token-only change, verified). The public release and the submission
   package are byte-identical. Earlier releases were left untouched.
5. **[Decision, recorded]** The manuscript's Use-of-LLM declarations
   were withdrawn for the submission version at the author's decision.
   Note for the record: the IJMLC/Springer guidance read on 14 October
   2026 requires LLM use beyond copy-editing assistance to be documented
   in the Methods section, with copy-editing-level assistance exempt;
   the withdrawn statements had described assistance beyond copy
   editing. Keeping this note here so the decision is on file with the
   author, who takes responsibility for disclosure choices.
6. **[Awareness]** The repository's `research-docs/` history (audit
   reports, revision logs) documents the full project workflow. If you
   prefer it less prominent, that is a separate repository-management
   decision (would require an authorised push); it has not been altered.
