#!/usr/bin/env python3
"""Download and parse MNIST + Fashion-MNIST into a single npz archive.

Sources (public mirrors):
- MNIST:   ossci-datasets S3 mirror used by torchvision
- Fashion-MNIST: zalandoresearch GitHub repository
IDX format: big-endian int32 header + unsigned byte payload.
"""
import gzip
import os
import struct
import sys
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

OUT = paths.DATA
os.makedirs(OUT, exist_ok=True)

SOURCES = {
    # name: url
    "mnist_train_x": "https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz",
    "mnist_train_y": "https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz",
    "mnist_test_x": "https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz",
    "mnist_test_y": "https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz",
    "fmnist_train_x": "https://github.com/zalandoresearch/fashion-mnist/raw/master/data/fashion/train-images-idx3-ubyte.gz",
    "fmnist_train_y": "https://github.com/zalandoresearch/fashion-mnist/raw/master/data/fashion/train-labels-idx1-ubyte.gz",
    "fmnist_test_x": "https://github.com/zalandoresearch/fashion-mnist/raw/master/data/fashion/t10k-images-idx3-ubyte.gz",
    "fmnist_test_y": "https://github.com/zalandoresearch/fashion-mnist/raw/master/data/fashion/t10k-labels-idx1-ubyte.gz",
}


def read_idx(url: str) -> np.ndarray:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = gzip.decompress(r.read())
    magic = struct.unpack(">I", raw[:4])[0]
    if magic == 2051:  # images
        n, rows, cols = struct.unpack(">III", raw[4:16])
        return np.frombuffer(raw[16:], dtype=np.uint8).reshape(n, rows * cols).copy()
    elif magic == 2049:  # labels
        n = struct.unpack(">I", raw[4:8])[0]
        return np.frombuffer(raw[8:], dtype=np.uint8).copy()
    raise ValueError(f"bad magic {magic} in {url}")


def main():
    arrays = {}
    for name, url in SOURCES.items():
        dest = os.path.join(OUT, name + ".npy")
        if os.path.exists(dest):
            arrays[name] = np.load(dest)
            print(f"cached {name} {arrays[name].shape}")
            continue
        arr = read_idx(url)
        np.save(dest, arr)
        arrays[name] = arr
        print(f"downloaded {name} {arr.shape}")

    np.savez_compressed(
        os.path.join(OUT, "datasets.npz"),
        **arrays,
    )
    # sanity checks
    fx, fy = arrays["fmnist_train_x"], arrays["fmnist_train_y"]
    mx, my = arrays["mnist_test_x"], arrays["mnist_test_y"]
    assert fx.shape == (60000, 784) and fy.shape == (60000,)
    assert mx.shape == (10000, 784) and my.shape == (10000,)
    assert fy.min() == 0 and fy.max() == 9
    print("pixel range:", fx.min(), fx.max())
    print("class balance (fmnist train):", np.bincount(fy))
    print("OK ->", os.path.join(OUT, "datasets.npz"))


if __name__ == "__main__":
    main()
