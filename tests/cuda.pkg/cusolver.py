#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The cusolver bindings factor and invert symmetric positive definite matrices, in both precisions
"""


def test():
    # support
    import numpy
    import pyre.cuda

    # the bindings
    cublas = pyre.cuda.cublas
    cusolver = pyre.cuda.cusolver
    # the triangle the routines read
    upper = cublas.FillMode.UPPER
    # a symmetric positive definite matrix
    n = 8
    rng = numpy.random.default_rng(2)
    x = rng.random((n, n))
    spd = x @ x.T + n * numpy.eye(n)
    # for each precision
    for prefix, cell, tolerance in (("d", "float64", 1e-10), ("s", "float32", 1e-4)):
        # a handle
        handle = cusolver.create()
        # the matrix on managed memory
        A = pyre.cuda.managed(shape=(n, n), cell=cell)
        numpy.asarray(A)[...] = spd
        # the status of each call
        info = pyre.cuda.managed(shape=(1,), cell="int32")
        # the workspace of the factorization
        lwork = getattr(cusolver, prefix + "potrf_buffer_size")(handle, upper, n, A, n)
        work = pyre.cuda.managed(shape=(max(lwork, 1),), cell=cell)
        # a row major lower factor is a column major upper one
        getattr(cusolver, prefix + "potrf")(handle, upper, n, A, n, work, lwork, info)
        assert numpy.allclose(
            numpy.tril(numpy.asarray(A)), numpy.linalg.cholesky(spd), atol=tolerance * n
        )
        # the workspace of the inversion
        lwork = getattr(cusolver, prefix + "potri_buffer_size")(handle, upper, n, A, n)
        work = pyre.cuda.managed(shape=(max(lwork, 1),), cell=cell)
        # invert, from the factor
        getattr(cusolver, prefix + "potri")(handle, upper, n, A, n, work, lwork, info)
        # only the lower triangle of the inverse is written, so mirror it
        inverse = numpy.tril(numpy.asarray(A)) + numpy.tril(numpy.asarray(A), -1).T
        assert numpy.allclose(inverse, numpy.linalg.inv(spd), atol=tolerance)
        # a matrix that is not positive definite is refused
        numpy.asarray(A)[...] = -numpy.eye(n)
        try:
            # so this
            getattr(cusolver, prefix + "potrf")(handle, upper, n, A, n, work, lwork, info)
        # raises
        except RuntimeError:
            # as it should
            pass
        # and anything else is a bug
        else:
            # so say so
            assert False, "cusolver factored a matrix that is not positive definite"
        # release the handle
        cusolver.destroy(handle)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
