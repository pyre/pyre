#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: the thin cublas bindings, over grids of cuda managed memory

cublas is column major; a row-major grid read back as column major is its transpose, so a
symmetric operand reads the same either way, while an asymmetric result (a product, a
triangular factor) comes back transposed from what a row-major caller expects. Rather than
hide that behind the bindings, each check below applies the swap by hand -- swap the operands,
swap their extents, keep the shared dimension -- exactly as a row-major caller of these thin
bindings must.
"""


def test():
    import numpy
    import pyre
    import pyre.grid
    import pyre.cuda

    cublas = pyre.cuda.cublas
    Op = cublas.Operation

    handle = cublas.create()

    # gemm: C(m,n) = A(m,k) B(k,n), row major, via the swap trick
    m, k, n = 4, 5, 3
    rng = numpy.random.default_rng(1)
    a = rng.random((m, k))
    b = rng.random((k, n))
    expected = a @ b

    A = pyre.grid.managed(shape=(m, k), cell="float64")
    B = pyre.grid.managed(shape=(k, n), cell="float64")
    C = pyre.grid.managed(shape=(m, n), cell="float64")
    numpy.asarray(A)[:, :] = a
    numpy.asarray(B)[:, :] = b

    cublas.dgemm(handle, Op.N, Op.N, n, m, k, 1.0, B, n, A, k, 0.0, C, n)
    assert numpy.allclose(numpy.asarray(C), expected)

    # gemmex: the same product, at {float32}; cublas only supports a handful of mixed
    # input/output combinations, so this exercises the dtype dispatch rather than mixing
    A32 = pyre.grid.managed(shape=(m, k), cell="float32")
    B32 = pyre.grid.managed(shape=(k, n), cell="float32")
    C32 = pyre.grid.managed(shape=(m, n), cell="float32")
    numpy.asarray(A32)[:, :] = a
    numpy.asarray(B32)[:, :] = b
    cublas.gemmex(handle, Op.N, Op.N, n, m, k, 1.0, B32, n, A32, k, 0.0, C32, n)
    assert numpy.allclose(numpy.asarray(C32), expected, atol=1e-5)

    # axpy: y = alpha x + y
    x = rng.random(10)
    y = rng.random(10)
    alpha = 2.5
    X = pyre.grid.managed(shape=(10,), cell="float64")
    Y = pyre.grid.managed(shape=(10,), cell="float64")
    numpy.asarray(X)[:] = x
    numpy.asarray(Y)[:] = y
    cublas.daxpy(handle, 10, alpha, X, 1, Y, 1)
    assert numpy.allclose(numpy.asarray(Y), alpha * x + y)

    # dtrmv: x = op(A) x, {A} lower triangular, row major, via the swap trick (ask for the
    # opposite triangle)
    n = 4
    L = numpy.tril(rng.random((n, n)))
    xv = rng.random(n)
    expected_xv = L @ xv

    Av = pyre.grid.managed(shape=(n, n), cell="float64")
    numpy.asarray(Av)[:, :] = L
    Xv = pyre.grid.managed(shape=(n,), cell="float64")
    numpy.asarray(Xv)[:] = xv
    cublas.dtrmv(handle, cublas.FillMode.UPPER, Op.T, cublas.DiagType.NON_UNIT, n, Av, n, Xv, 1)
    assert numpy.allclose(numpy.asarray(Xv), expected_xv)

    # dsymm: C = alpha A B + beta C, {A} symmetric, row major (symmetric, so no swap needed
    # for {A} itself; the product is not symmetric, so the swap trick still applies overall)
    sym = rng.random((n, n))
    sym = sym + sym.T
    rhs = rng.random((n, n + 1))
    expected_symm = sym @ rhs

    As = pyre.grid.managed(shape=(n, n), cell="float64")
    numpy.asarray(As)[:, :] = sym
    Bs = pyre.grid.managed(shape=(n, n + 1), cell="float64")
    numpy.asarray(Bs)[:, :] = rhs
    Cs = pyre.grid.managed(shape=(n, n + 1), cell="float64")
    # C(m,n) = A(m,m) B(m,n) row major -> swap to C^T(n,m) = B^T(n,m) A^T(m,m); {A}
    # symmetric so A^T=A needs no separate handling beyond the side/shape swap
    cublas.dsymm(
        handle, cublas.SideMode.RIGHT, cublas.FillMode.LOWER, n + 1, n, 1.0, As, n, Bs, n + 1,
        0.0, Cs, n + 1)
    assert numpy.allclose(numpy.asarray(Cs), expected_symm)

    cublas.destroy(handle)

    # cusolver: cholesky and inverse of a symmetric positive definite matrix
    cusolver = pyre.cuda.cusolver
    spd = L @ L.T + n * numpy.eye(n)

    Aspd = pyre.grid.managed(shape=(n, n), cell="float64")
    numpy.asarray(Aspd)[:, :] = spd

    solver = cusolver.create()
    # UPPER on the way in gives back a row-major LOWER factor, the same swap trick as above
    lwork = cusolver.dpotrf_buffer_size(solver, cublas.FillMode.UPPER, n, Aspd, n)
    workspace = pyre.grid.managed(shape=(max(lwork, 1),), cell="float64")
    info = pyre.grid.managed(shape=(1,), cell="int32")
    cusolver.dpotrf(solver, cublas.FillMode.UPPER, n, Aspd, n, workspace, lwork, info)

    factor = numpy.tril(numpy.asarray(Aspd))
    assert numpy.allclose(factor, numpy.linalg.cholesky(spd))

    lwork = cusolver.dpotri_buffer_size(solver, cublas.FillMode.UPPER, n, Aspd, n)
    workspace = pyre.grid.managed(shape=(max(lwork, 1),), cell="float64")
    info = pyre.grid.managed(shape=(1,), cell="int32")
    cusolver.dpotri(solver, cublas.FillMode.UPPER, n, Aspd, n, workspace, lwork, info)

    # only the lower triangle of the inverse was written; mirror it before comparing
    inverse = numpy.asarray(Aspd).copy()
    upper = numpy.triu_indices(n, k=1)
    inverse[upper] = inverse[(upper[1], upper[0])]
    assert numpy.allclose(inverse, numpy.linalg.inv(spd), atol=1e-8)

    cusolver.destroy(solver)

    # curand: fill grids straight from a device generator
    curand = pyre.cuda.curand
    generator = curand.create_generator(curand.RngType.DEFAULT)
    curand.set_seed(generator, 2026)

    uniform = pyre.grid.managed(shape=(100,), cell="float64")
    curand.generate_uniform_double(generator, uniform, 100)
    values = numpy.asarray(uniform)
    assert values.min() >= 0.0 and values.max() <= 1.0

    normal = pyre.grid.managed(shape=(10000,), cell="float64")
    curand.generate_normal_double(generator, normal, 10000, 0.0, 1.0)
    values = numpy.asarray(normal)
    assert abs(values.mean()) < 0.1
    assert abs(values.std() - 1.0) < 0.1

    curand.destroy_generator(generator)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
