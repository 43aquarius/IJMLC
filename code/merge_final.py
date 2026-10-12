#!/usr/bin/env python3
"""Merge HTML cover (page 0) with the LaTeX body, normalizing to A4 + metadata."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89  # A4 in points


writer = PdfWriter()
import paths
cover_page = PdfReader(os.path.join(paths.ROOT, "paper", "cover.pdf")).pages[0]
cover_page.scale_to(A4_W, A4_H)  # always normalize (QA tolerance is strict)
writer.add_page(cover_page)
for page in PdfReader(os.path.join(paths.ROOT, "paper", "main.pdf")).pages:
    page.scale_to(A4_W, A4_H)
    writer.add_page(page)

writer.add_metadata({
    "/Title": "Budget-split deep ensembles outperform snapshot ensembles and weight "
              "averaging for calibrated uncertainty",
    "/Author": "Z.ai",
    "/Creator": "Qinyan Nature Skills workflow (LaTeX/Tectonic)",
    "/Subject": "Budget-matched comparison of ensemble strategies for predictive uncertainty",
    "/Keywords": "deep ensembles, snapshot ensembles, stochastic weight averaging, "
                 "calibration, uncertainty quantification, budget-matched evaluation",
})
with open(os.path.join(paths.ROOT, "paper", "final.pdf"), "wb") as f:
    writer.write(f)
print("merged -> final.pdf, pages:", len(writer.pages))
