#!/usr/bin/env python3
"""Build datasets_v2.npz: v1 datasets + KMNIST test probe.

Reuses the existing v1 datasets.npz byte-for-byte (so the Fashion-MNIST
and MNIST arrays stay bit-identical to v1), and only adds the KMNIST
test set as an additional OOD probe (Clanuwat et al. 2018).

KMNIST is fetched directly from the official ROIS-CODH mirror (HTTPS),
so no torchvision dependency is required.
"""
import gzip
import os
import struct
import sys
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

SRC = paths.DATASETS_V1
OUT = paths.DATASETS_V2
KRAW = os.path.join(paths.DATA, "kmnist", "KMNIST", "raw")

BASE = "https://codh.rois.ac.jp/kmnist/dataset/kmnist/"
FILES = ["t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]


def _read_idx(raw: bytes):
    """Minimal IDX parser: big-endian header + unsigned byte payload."""
    magic = struct.unpack(">HBB", raw[:4])
    ndim = magic[2]
    dims = struct.unpack(f">{ndim}I", raw[4:4 + 4 * ndim])
    return np.frombuffer(raw[4 + 4 * ndim:], dtype=np.uint8).reshape(dims)


os.makedirs(KRAW, exist_ok=True)
arrs = {}
for fn in FILES:
    dst = os.path.join(KRAW, fn)
    if not os.path.exists(dst):
        print("downloading", BASE + fn)
        urllib.request.urlretrieve(BASE + fn, dst)
    with gzip.open(dst, "rb") as f:
        arrs[fn] = _read_idx(f.read())

kx = arrs[FILES[0]]
ky = arrs[FILES[1]]
assert kx.shape == (10000, 28, 28) and ky.shape == (10000,), (kx.shape, ky.shape)

d = np.load(SRC)
out = {k: d[k] for k in d.files}
out["kmnist_test_x"] = kx.reshape(-1, 784).astype(np.uint8)
out["kmnist_test_y"] = ky.astype(np.uint8)

np.savez_compressed(OUT, **out)

chk = np.load(OUT)
print("saved:", OUT)
for k in ["fmnist_train_x", "mnist_train_x", "kmnist_test_x"]:
    print(f"  {k}: {chk[k].shape}")
# bit-identity check against v1 for the original arrays
same = all(np.array_equal(d[k], chk[k]) for k in d.files)
print("v1 arrays bit-identical:", same)
print("kmnist class counts:", np.bincount(chk["kmnist_test_y"]))
