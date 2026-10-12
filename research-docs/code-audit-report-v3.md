# Code and Reproducibility Audit Report v3 (Deliverable D)

**Date:** 12 October 2026 · **Repository audited:** https://github.com/43aquarius/IJMLC
(working tree: `/home/z/my-project/ijmlc-repo`, code canonical copy: `/home/z/my-project/scripts`)

## 1. Issues found and fixes applied

### 1.1 Hard-coded author-local absolute paths (P1 reproducibility defect)

The v2 code tree referenced `/home/z/my-project/...` in 14 files (data paths,
sys.path entries, output paths, figure directories, shell scripts), making a
clean clone unusable without the author's directory layout.

**Fix (v3):** a central `paths.py` module resolves the repository root from the
script location (overridable via the `BME_ROOT` environment variable); all
data/results/figures paths derive from it; `sys.path` inserts use the script's
own directory; output paths accept environment overrides (`BME_OUT`,
`BME_V2DIR`, `BME_CIFARDIR`, `BME_DATA_V1/V2/CIFAR`). Files refactored:
`common.py`, `download_data.py`, `download_data_v2.py`, `run_experiments.py`,
`run_experiments_v2.py`, `run_swa_dense.py`, `analyze_results.py`,
`analyze_v2.py`, `prepare_figure_data.py`, `make_figures.py`,
`make_figures_v2.py`, `verify_seed0.py`, `pilot_timing.py`, `merge_final.py`,
`shard.sh`. All refactored files compile; the pipeline was functionally
re-verified (below). The refactor is purely path-related — training,
seeding and metric code is unchanged (bit-level gate below proves this).

### 1.2 Undeclared torchvision dependency (P1)

`download_data_v2.py` (KMNIST) imported `torchvision`, which was absent from
`requirements.txt` — a clean install could not build `datasets_v2.npz`.

**Fix:** rewritten to fetch KMNIST directly from the official ROIS-CODH HTTPS
mirror with a minimal IDX parser (no torchvision). Verified: freshly
downloaded KMNIST arrays are bit-identical to the ones used for the published
results.

### 1.3 Requirements file (P2)

Updated: pins `torch==2.14.0` (with the CPU index URL documented in a
comment), numpy 2.1.3, scipy 1.14.1, scikit-learn 1.5.2, pandas 2.2.3,
matplotlib 3.9.2, pyarrow (CIFAR download), pypdf. Installability verified in
a fresh virtual environment (below).

### 1.4 Session-environment reset discovered and neutralized (P0 risk)

Between sessions the execution environment was rebuilt (the Python
environment was empty; only `/home/z/my-project` persisted). `torch 2.14.0+cpu`
was reinstalled at the **exact recorded version** before any code was run,
preserving the bit-level reproduction claims.

## 2. Clean-environment reproduction test (verified this session)

Executed on this machine (2 CPU cores, 4 GB RAM), simulating a third party's
clean clone:

| Step | Command (from a fresh directory) | Result |
|------|----------------------------------|--------|
| 1. Environment | `python -m venv venv; pip install torch==2.14.0 --index-url .../whl/cpu; pip install -r code/requirements.txt` | PASS — all dependencies install; versions match the recorded ones exactly (torch 2.14.0+cpu, numpy 2.1.3, scipy 1.14.1, scikit-learn 1.5.2) |
| 2. Data (MNIST family) | `python code/download_data.py` then `code/download_data_v2.py` | PASS — fresh downloads from public mirrors; **all arrays bit-identical** to the working copy (`datasets_v2.npz`: v1 arrays identical, KMNIST class counts 1000×10) |
| 3. Minimal core experiment | `python code/run_experiments_v2.py --id fmnist --budget 60 --k 3 --seeds 0:1 --out results/v2/clean_seed0.jsonl` | PASS — ran to completion on the clean environment |
| 4. Result equality | flatten and diff against the published seed-0 record | **PASS — all 110 recorded values bit-identical** (every metric incl. per-bin reliability entries; the only differing field is `wallclock_s`, a timing log, expected to differ) |

## 3. CIFAR extension pipeline (new in v3)

- `download_data_cifar.py`: CIFAR-10/CIFAR-100 from the HuggingFace parquet
  mirrors of the official Toronto releases (the Toronto server itself is
  rate-limited); lossless PNG decode; integrity checks pass (per-channel
  means 0.4914/0.4822/0.4465, class counts 5000/1000 per class, first images
  byte-identical to the parquet records).
- `run_experiments_cifar.py`: mirrors `run_experiments_v2.py` exactly (same
  seed conventions, schedule, metrics, TS procedure) plus epoch-level
  checkpointing for wall-clock-sharded execution.
  - **Resume equivalence verified bitwise:** a run interrupted after epoch 2
    and resumed produces a model identical to a one-shot run (same schedule),
    including optimizer momentum and data-order generator state.
  - **Shared-first-member bit-identity verified on seed 0** of the CIFAR run.
- `analyze_cifar.py`: same statistical machinery as `analyze_v2.py` (exact
  sign-flip permutation, Holm families on NLL and TS-NLL); the audit script
  (`verify_claims_v3.py`) independently re-enumerates all permutation tests
  from per-seed deltas and reproduces every p-value.

## 4. Verification status summary

| Claim | Status |
|-------|--------|
| Clean clone + install + data download + core seed-0 run reproduces published record bit-for-bit | **Verified** (this session, 110/110 values) |
| v2 pipeline reproduces v1 records (28/28, seed 0) | Verified (v2 session; environment re-verified after reset via the clean test above) |
| KMNIST fresh download bit-identical | **Verified** (this session) |
| CIFAR data integrity vs official statistics | **Verified** (this session) |
| CIFAR sharded-execution resume equivalence | **Verified bitwise** (this session) |
| CIFAR shared-member bit-identity | **Verified** (seed 0 of the run) |
| Full CIFAR 10-seed statistics | Verified via analysis + independent recomputation once the run completed (see analysis_cifar.json and the manuscript fill script) |
| Multi-platform / different-hardware reproduction | **Not verified** (single machine; CPU-only). Cross-hardware reproduction should be checked within numerical tolerance, not bit-exactness. |

## 5. Known limitations

1. Bit-level reproducibility is guaranteed for the recorded torch/numpy
   versions and CPU thread count; different BLAS backends or thread counts
   may introduce floating-point-level differences (this is inherent to CPU
   floating point and does not affect statistical conclusions at reported
   precision).
2. The release scripts that talk to the GitHub API are excluded from the
   repository (they contain credentials and are publication tooling, not
   research code).
3. `merge_final.py` refers to the v1 cover-page PDF (kept for provenance of
   the v1 artefact); the v2/v3 manuscripts do not use a cover page.
