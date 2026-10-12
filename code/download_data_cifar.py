#!/usr/bin/env python3
"""Download CIFAR-10 / CIFAR-100 via the HuggingFace parquet mirror
(uoft-cs/cifar10, uoft-cs/cifar100 -- lossless PNG encodings of the original
Krizhevsky binaries) and store as .npz in the MNIST-family convention.

Provenance note: the HF datasets are byte-identical in content to the
official https://www.cs.toronto.edu/~kriz/ releases (PNG is lossless);
we verify per-channel means against the published CIFAR-10 statistics
(0.4914, 0.4822, 0.4465) and per-class counts as integrity checks.
"""
import io
import os
import sys

import numpy as np
import pyarrow.parquet as pq
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

BASE10 = "https://huggingface.co/datasets/uoft-cs/cifar10/resolve/main/plain_text"
BASE100 = "https://huggingface.co/datasets/uoft-cs/cifar100/resolve/main/cifar100"
OUT = paths.DATASETS_CIFAR

def fetch(url, cache):
    import urllib.request
    if not _exists(cache):
        print("downloading", url, flush=True)
        urllib.request.urlretrieve(url, cache)
    return cache

def _exists(p):
    import os
    return os.path.exists(p)

def decode_images(table):
    imgs = table["img"]
    n = len(imgs)
    out = np.zeros((n, 32, 32, 3), dtype=np.uint8)
    for i in range(n):
        d = imgs[i]
        d = d["bytes"] if isinstance(d, dict) else d
        out[i] = np.asarray(Image.open(io.BytesIO(d)).convert("RGB"))
    return out

import os, urllib.request
HF = os.path.join(paths.DATA, "hf")
os.makedirs(HF, exist_ok=True)

files = {
    "c10_train": f"{BASE10}/train-00000-of-00001.parquet",
    "c10_test": f"{BASE10}/test-00000-of-00001.parquet",
    "c100_test": f"{BASE100}/test-00000-of-00001.parquet",
}
paths = {}
for name, url in files.items():
    cache = os.path.join(HF, f"{name}.parquet")
    if not os.path.exists(cache):
        print("downloading", url, flush=True)
        urllib.request.urlretrieve(url, cache)
    paths[name] = cache

tr = pq.read_table(paths["c10_train"]).to_pydict()
te = pq.read_table(paths["c10_test"]).to_pydict()
c100 = pq.read_table(paths["c100_test"]).to_pydict()

tr_x = decode_images(tr); tr_y = np.asarray(tr["label"], dtype=np.int64)
te_x = decode_images(te); te_y = np.asarray(te["label"], dtype=np.int64)
c100_x = decode_images(c100); c100_y = np.asarray(c100["fine_label"], dtype=np.int64)

out = dict(
    cifar10_train_x=tr_x, cifar10_train_y=tr_y,
    cifar10_test_x=te_x,  cifar10_test_y=te_y,
    cifar100_test_x=c100_x, cifar100_test_y=c100_y,
)
np.savez_compressed(OUT, **out)
print("saved", OUT)
for k, v in out.items():
    print(f"  {k}: {v.shape} {v.dtype} range=[{v.min()},{v.max()}]")
print("train class counts:", np.bincount(tr_y))
print("test  class counts:", np.bincount(te_y))
print("c100 fine labels in [0,100):", c100_y.min(), c100_y.max())
chan = tr_x.astype(np.float32).mean(axis=(0, 1, 2)) / 255.0
print("per-channel means (want ~0.4914 0.4822 0.4465):", np.round(chan, 4))
