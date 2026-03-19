#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2026 all rights reserved


"""
Verify the DLPack interface for gsl.vector and gsl.matrix
"""


def test():
    # package access
    import gsl

    # --- vector ---
    v = gsl.vector(shape=10)
    # fill with known values
    for i in range(10):
        v[i] = float(i)

    # device must be (kDLCPU=1, device_id=0)
    device = v.data.__dlpack_device__()
    assert device == (1, 0), f"unexpected device: {device}"

    # consume the DLPack capsule via numpy
    import numpy as np
    arr = np.from_dlpack(v.data)
    assert arr.shape == (10,), f"unexpected shape: {arr.shape}"
    assert arr.dtype == np.float64, f"unexpected dtype: {arr.dtype}"
    for i in range(10):
        assert arr[i] == float(i), f"value mismatch at {i}: {arr[i]}"

    # modifications through the DLPack view are visible in the original (zero-copy)
    arr[0] = 99.0
    assert v[0] == 99.0, "DLPack array is not a zero-copy view of the vector"

    # --- matrix ---
    m = gsl.matrix(shape=(4, 5))
    for i in range(4):
        for j in range(5):
            m[i, j] = float(i * 5 + j)

    device = m.data.__dlpack_device__()
    assert device == (1, 0), f"unexpected device: {device}"

    mat = np.from_dlpack(m.data)
    assert mat.shape == (4, 5), f"unexpected shape: {mat.shape}"
    assert mat.dtype == np.float64, f"unexpected dtype: {mat.dtype}"
    for i in range(4):
        for j in range(5):
            assert mat[i, j] == float(i * 5 + j), f"value mismatch at ({i},{j})"

    # zero-copy check
    mat[0, 0] = -1.0
    assert m[0, 0] == -1.0, "DLPack array is not a zero-copy view of the matrix"

    # all done
    return v, m


# main
if __name__ == "__main__":
    test()


# end of file
