#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The cublas bindings agree with numpy, in both precisions
"""


def test():
    # support
    import numpy
    import pyre.cuda

    # the bindings
    cublas = pyre.cuda.cublas
    # the orientation of the operands
    Op = cublas.Operation
    # some random numbers
    rng = numpy.random.default_rng(1)
    # for each precision
    for prefix, cell, tolerance in (("d", "float64", 1e-10), ("s", "float32", 1e-5)):
        # a handle
        handle = cublas.create()
        # the operands of a product, row major
        m, k, n = 4, 5, 3
        a = rng.random((m, k))
        b = rng.random((k, n))
        # on managed memory
        A = pyre.cuda.managed(shape=(m, k), cell=cell)
        B = pyre.cuda.managed(shape=(k, n), cell=cell)
        C = pyre.cuda.managed(shape=(m, n), cell=cell)
        numpy.asarray(A)[...] = a
        numpy.asarray(B)[...] = b
        # a row major product is the column major product of the transposes, swapped
        getattr(cublas, prefix + "gemm")(handle, Op.N, Op.N, n, m, k, 1.0, B, n, A, k, 0.0, C, n)
        assert numpy.allclose(numpy.asarray(C), a @ b, atol=tolerance)
        # gemmex picks the precision from the cells
        cublas.gemmex(handle, Op.N, Op.N, n, m, k, 1.0, B, n, A, k, 0.0, C, n)
        assert numpy.allclose(numpy.asarray(C), a @ b, atol=tolerance)
        # y = alpha x + y
        x = pyre.cuda.managed(shape=(10,), cell=cell)
        y = pyre.cuda.managed(shape=(10,), cell=cell)
        numpy.asarray(x)[...] = numpy.arange(10)
        numpy.asarray(y)[...] = 1
        getattr(cublas, prefix + "axpy")(handle, 10, 2.5, x, 1, y, 1)
        assert numpy.allclose(numpy.asarray(y), 2.5 * numpy.arange(10) + 1, atol=tolerance)
        # x = L x, with a row major lower triangle read as a column major upper one
        lower = numpy.tril(rng.random((4, 4)))
        v = rng.random(4)
        L = pyre.cuda.managed(shape=(4, 4), cell=cell)
        X = pyre.cuda.managed(shape=(4,), cell=cell)
        numpy.asarray(L)[...] = lower
        numpy.asarray(X)[...] = v
        getattr(cublas, prefix + "trmv")(
            handle, cublas.FillMode.UPPER, Op.T, cublas.DiagType.NON_UNIT, 4, L, 4, X, 1
        )
        assert numpy.allclose(numpy.asarray(X), lower @ v, atol=tolerance)
        # release the handle
        cublas.destroy(handle)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
