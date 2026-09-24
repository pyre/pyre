#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

"""
pyre.grid with cuTile ({cuda.tile}): tile kernels written in python, over managed grids

cuTile partitions an array into a space of equally sized tiles and lets a block load, compute
on, and store whole tiles; it indexes row major, the same way pyre grids and numpy do, so no
operand swapping is needed. It takes arrays through {__dlpack__} or {__cuda_array_interface__}:
its dlpack path accepts device memory only ({kDLCUDA}) and turns down managed memory, which a
pyre grid correctly reports as {kDLCUDAManaged}, so managed grids go in through the cuda array
interface; {cai} below is the adapter that offers that, and only that

cuTile also recognizes cupy and torch streams by type, but takes any other stream as its raw
handle, so a {cuda.core} stream goes in as {int(stream.handle)}

needs pyre built {WITH_CUDA}, {cuda-core}, and {cuda-tile}
"""

import numpy
import pyre.grid
import cuda.tile as ct
from cuda.core import Device


class cai:
    """Present a grid to cuTile through its cuda array interface only"""

    def __init__(self, grid):
        # hold on to the grid, which owns the cells the interface points at
        self.grid = grid
        self.__cuda_array_interface__ = grid.__cuda_array_interface__


def managed(shape, cell="float32"):
    """A fresh grid on managed memory"""
    return pyre.grid.managed(shape=shape, cell=cell)


# y = a x + y, one (tm, tn) tile per block
@ct.kernel
def axpy(a, x, y, tm: ct.Constant[int], tn: ct.Constant[int]):
    i, j = ct.bid(0), ct.bid(1)
    tx = ct.load(x, index=(i, j), shape=(tm, tn))
    ty = ct.load(y, index=(i, j), shape=(tm, tn))
    ct.store(y, index=(i, j), tile=a * tx + ty)


# s = the row sums of x, one strip of tm rows per block, walking across the columns
@ct.kernel
def rowsum(x, s, tm: ct.Constant[int], tn: ct.Constant[int]):
    i = ct.bid(0)
    acc = ct.zeros((tm,), dtype=ct.float32)
    for j in range(ct.num_tiles(x, 1, shape=(tm, tn))):
        # the cells past the last column read as zero, so they add nothing
        tile = ct.load(x, index=(i, j), shape=(tm, tn), padding_mode=ct.PaddingMode.ZERO)
        acc += ct.sum(tile, axis=1)
    ct.store(s, index=(i,), tile=acc)


# c = a b, one (tm, tn) tile of c per block, accumulating over the (tm, tk) x (tk, tn) products
@ct.kernel
def matmul(a, b, c, tm: ct.Constant[int], tn: ct.Constant[int], tk: ct.Constant[int]):
    i, j = ct.bid(0), ct.bid(1)
    acc = ct.zeros((tm, tn), dtype=ct.float32)
    for k in range(ct.num_tiles(a, 1, shape=(tm, tk))):
        # zero padding past the edges keeps partial tiles out of the product
        ta = ct.load(a, index=(i, k), shape=(tm, tk), padding_mode=ct.PaddingMode.ZERO)
        tb = ct.load(b, index=(k, j), shape=(tk, tn), padding_mode=ct.PaddingMode.ZERO)
        acc = ct.mma(ta, tb, acc)
    ct.store(c, index=(i, j), tile=acc)


def main():
    device = Device()
    device.set_current()
    stream = device.create_stream()
    handle = int(stream.handle)
    rng = numpy.random.default_rng(0)

    # sizes that are deliberately not multiples of the tiles
    m, k, n = 1000, 700, 900
    tm, tn, tk = 64, 64, 32

    # axpy over two grids
    x, y = managed((m, n)), managed((m, n))
    numpy.asarray(x)[...] = rng.random((m, n))
    numpy.asarray(y)[...] = rng.random((m, n))
    expected = 2.5 * numpy.asarray(x) + numpy.asarray(y)
    ct.launch(handle, (ct.cdiv(m, tm), ct.cdiv(n, tn), 1), axpy, (2.5, cai(x), cai(y), tm, tn))
    stream.sync()
    error = numpy.abs(numpy.asarray(y) - expected).max()
    print(f"axpy    grid{y.shape}: max error {error:.3e}")

    # row sums of a grid into another
    s = managed((m,))
    ct.launch(handle, (ct.cdiv(m, tm), 1, 1), rowsum, (cai(x), cai(s), tm, tn))
    stream.sync()
    error = numpy.abs(numpy.asarray(s) - numpy.asarray(x).sum(axis=1)).max()
    print(f"rowsum  grid{s.shape}: max error {error:.3e}")

    # the product of two grids into a third
    a, b, c = managed((m, k)), managed((k, n)), managed((m, n))
    numpy.asarray(a)[...] = rng.random((m, k))
    numpy.asarray(b)[...] = rng.random((k, n))
    ct.launch(handle, (ct.cdiv(m, tm), ct.cdiv(n, tn), 1), matmul, (cai(a), cai(b), cai(c), tm, tn, tk))
    stream.sync()
    expected = numpy.asarray(a).astype(numpy.float64) @ numpy.asarray(b).astype(numpy.float64)
    error = numpy.abs(numpy.asarray(c) - expected).max() / numpy.abs(expected).max()
    print(f"matmul  grid{c.shape}: max relative error {error:.3e}")


if __name__ == "__main__":
    main()


# end of file
