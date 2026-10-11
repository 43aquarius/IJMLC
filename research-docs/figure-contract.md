# Figure Contract (qinyan-nature-figures)

**Figure 1 (main, double-column 183 mm × ~140 mm, 5 panels a–e)**

1. **Conclusion**: At a fixed training budget, ensembling independently restarted short runs (DeepEns) gives the best accuracy, calibration and OOD detection; cyclic-LR snapshot ensembles are intermediate because continued training makes members overconfident and correlated; weight averaging (SWA) improves in-distribution metrics but not OOD detection; prediction-averaging the same three checkpoints beats weight-averaging them.

2. **Evidence hierarchy**:
   - Main: paired NLL across 10 seeds (panel b); OOD AUROC (panel d).
   - Mechanism/support: member calibration + ensemble diversity (panel e); reliability diagrams (panel c).
   - Design/control: LR schedules showing identical budget (panel a).

3. **Panel map**:

| Panel | Question | Data | Graph | Statistics | Reader takeaway |
|---|---|---|---|---|---|
| a | How is the budget allocated? | exact LR schedules used in training | line plot, 2 trajectories + markers | none (design) | same 60-epoch budget, three allocations |
| b | Which allocation yields lowest NLL? | test NLL, 10 seeds × 4 conditions | paired dot-line plot (thin lines = seeds, large markers = mean) | paired by seed; n=10 | DeepEns < Snapshot < SWA < Single |
| c | Are ensembles better calibrated? | reliability diagrams (15 bins), mean over seeds | bin-acc vs bin-conf curves + diagonal | n=10 seeds aggregated | Single overconfident; DeepEns closest to diagonal |
| d | Does it improve OOD detection? | AUROC-MSP (MNIST probe), 10 seeds × 4 conditions | paired dot-line plot | paired by seed; n=10 | DeepEns +0.10; SWA ≈ Single (no gain) |
| e | Why does DeepEns beat Snapshot? | member mean NLL + pairwise JSD, 10 seeds × 2 conditions | two mini dot plots with all seed points | descriptive | fresh restarts: better-calibrated members + higher diversity |

4. **Data contract**: one row = one (seed, condition) summary from results/experiment.jsonl; independent unit = seed (n=10); no exclusions; no transformations beyond those logged in the analysis; reliability bins: 15 equal-width; OOD score: max-softmax.

5. **Statistics contract**: panels b/d/e show all 10 seed-level observations (no error-bar-only displays); means marked; Holm-adjusted exact permutation p reported in text/tables, not stars on figures; CIs in tables; figures carry no p-value stars.

6. **Export contract**: main figure 183 mm wide; font: Arial/Helvetica ≥ 6 pt at final size (target 7–8 pt); vector PDF (primary) + 600 dpi PNG (preview); colourblind-safe Okabe–Ito palette; condition colours fixed globally: Single #8C8C8C, DeepEns #0072B2, Snapshot #E69F00, SWA #009E73; shape redundancy (○ ● ■ ◆) in addition to colour; panel letters 8 pt bold lowercase.

**Supplementary figures (single-column 89 mm each)**

- **Suppl. Fig. 1**: reliability diagrams per condition with per-seed variability (small multiples, 4 panels).
- **Suppl. Fig. 2**: max-softmax score distributions, in-distribution vs OOD, per condition (4 panels, mean histograms over seeds) — visual explanation of AUROC differences.
- **Suppl. Fig. 3**: SWA-dense supplementary condition (exploratory): NLL + AUROC paired dots vs pre-registered conditions.
- **Suppl. Fig. 4**: validation NLL learning curves of the two training trajectories (single cosine vs cyclic), mean ± s.d. over seeds, with cycle boundaries marked.

**Supplementary tables**

- **Suppl. Table 1**: all metrics per condition (mean ± s.d., n=10, all seed values in source data).
- **Suppl. Table 2**: all five contrasts × five metrics: mean Δ, 95% CI, exact permutation p, Holm-adjusted p (NLL family).
- **Suppl. Table 3**: SWA-dense exploratory summary.

**Source data**: one CSV per figure panel (NLL/AUROC/JSD per seed per condition; reliability bin data; histograms; LR schedule values).
