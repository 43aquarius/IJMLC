"""Centralised path resolution for the budget-matched ensembles project.

All scripts resolve paths relative to the repository root (the parent of the
directory containing this file), so a clean clone works without any
author-local directory structure. Override the root with the BME_ROOT
environment variable to relocate data/results/figures elsewhere.
"""
import os

ROOT = os.environ.get(
    "BME_ROOT",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)


def p(*parts):
    """Join ROOT with the given path parts."""
    return os.path.join(ROOT, *parts)


# canonical locations
RESULTS = p("results")
DATA = p("results", "data")
FIGURES = p("figures")
DATASETS_V1 = os.environ.get("BME_DATA_V1", p("results", "data", "datasets.npz"))
DATASETS_V2 = os.environ.get("BME_DATA_V2", p("results", "data", "datasets_v2.npz"))
DATASETS_CIFAR = os.environ.get(
    "BME_DATA_CIFAR", p("results", "data", "datasets_cifar.npz"))
