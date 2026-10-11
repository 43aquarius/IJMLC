#!/usr/bin/env python3
"""Build datasets_v2.npz: v1 datasets + KMNIST test probe.

Reuses the existing v1 datasets.npz byte-for-byte (so the Fashion-MNIST
and MNIST arrays stay bit-identical to v1), and only adds the KMNIST
test set as an additional OOD probe (Clanuwat et al. 2018).
"""
import numpy as np

SRC = "/home/z/my-project/results/data/datasets.npz"
OUT = "/home/z/my-project/results/data/datasets_v2.npz"

import torchvision
from torchvision.datasets import KMNIST

# the environment blocks plain-HTTP egress; force the HTTPS mirror
KMNIST.mirrors = ["https://codh.rois.ac.jp/kmnist/dataset/kmnist/"]

# download KMNIST test only
km = KMNIST(root="/home/z/my-project/results/data/kmnist",
            train=False, download=True)
kx = np.asarray(km.data.reshape(-1, 784), dtype=np.uint8)
ky = np.asarray(km.targets, dtype=np.uint8)

d = np.load(SRC)
out = {k: d[k] for k in d.files}
out["kmnist_test_x"] = kx
out["kmnist_test_y"] = ky

np.savez_compressed(OUT, **out)

chk = np.load(OUT)
print("saved:", OUT)
for k in ["fmnist_train_x", "mnist_train_x", "kmnist_test_x"]:
    print(f"  {k}: {chk[k].shape}")
# bit-identity check against v1 for the original arrays
same = all(np.array_equal(d[k], chk[k]) for k in d.files)
print("v1 arrays bit-identical:", same)
print("kmnist class counts:", np.bincount(chk["kmnist_test_y"]))
