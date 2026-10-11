#!/usr/bin/env python3
"""Merge HTML cover (page 0) with the LaTeX body, normalizing to A4 + metadata."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89  # A4 in points


writer = PdfWriter()
cover_page = PdfReader("/home/z/my-project/paper/cover.pdf").pages[0]
cover_page.scale_to(A4_W, A4_H)  # always normalize (QA tolerance is strict)
writer.add_page(cover_page)
for page in PdfReader("/home/z/my-project/paper/main.pdf").pages:
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
with open("/home/z/my-project/paper/final.pdf", "wb") as f:
    writer.write(f)
print("merged -> final.pdf, pages:", len(writer.pages))
