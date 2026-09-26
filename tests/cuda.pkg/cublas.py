#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: the thin cublas/cusolver/curand bindings, over grids of cuda managed memory,
at both {float64} and {float32}

cublas/cusolver are column major; a row-major grid read back as column major is its transpose,
so a symmetric operand reads the same either way, while an asymmetric result (a product, a
triangular factor) comes back transposed from what a row-major caller expects. Rather than hide
that behind the bindings, each check below applies the swap by hand -- swap the operands, swap
their extents, keep the shared dimension -- exactly as a row-major caller of these thin bindings
must.
"""


def check(precision):
    import numpy
    import pyre
    import pyre.grid
    import pyre.cuda

    cublas = pyre.cuda.cublas
    cusolver = pyre.cuda.cusolver
    Op = cublas.Operation

    # the routine suffix and comparison tolerance for this precision
    suffix = "d" if precision == "float64" else "s"
    tol = 1e-8 if precision == "float64" else 1e-5

    def grid(shape):
        return pyre.grid.managed(shape=shape, cell=precision)

    handle = cublas.create()

    # gemm: C(m,n) = A(m,k) B(k,n), row major, via the swap trick
    m, k, n = 4, 5, 3
    rng = numpy.random.default_rng(1)
    a = rng.random((m, k))
    b = rng.random((k, n))
    expected = a @ b

    A = grid((m, k))
    B = grid((k, n))
    C = grid((m, n))
    numpy.asarray(A)[:, :] = a
    numpy.asarray(B)[:, :] = b

    getattr(cublas, suffix + "gemm")(handle, Op.N, Op.N, n, m, k, 1.0, B, n, A, k, 0.0, C, n)
    assert numpy.allclose(numpy.asarray(C), expected, atol=tol)

    # gemmex, at this same precision throughout: exercises the dtype dispatch
    cublas.gemmex(handle, Op.N, Op.N, n, m, k, 1.0, B, n, A, k, 0.0, C, n)
    assert numpy.allclose(numpy.asarray(C), expected, atol=tol)

    # axpy: y = alpha x + y
    x = rng.random(10)
    y = rng.random(10)
    alpha = 2.5
    X = grid((10,))
    Y = grid((10,))
    numpy.asarray(X)[:] = x
    numpy.asarray(Y)[:] = y
    getattr(cublas, suffix + "axpy")(handle, 10, alpha, X, 1, Y, 1)
    assert numpy.allclose(numpy.asarray(Y), alpha * x + y, atol=tol)

    # trmv: x = op(A) x, {A} lower triangular, row major, via the swap trick (ask for the
    # opposite triangle)
    n = 4
    L = numpy.tril(rng.random((n, n)))
    xv = rng.random(n)
    expected_xv = L @ xv

    Av = grid((n, n))
    numpy.asarray(Av)[:, :] = L
    Xv = grid((n,))
    numpy.asarray(Xv)[:] = xv
    getattr(cublas, suffix + "trmv")(
        handle, cublas.FillMode.UPPER, Op.T, cublas.DiagType.NON_UNIT, n, Av, n, Xv, 1)
    assert numpy.allclose(numpy.asarray(Xv), expected_xv, atol=tol)

    # symm: C = alpha A B + beta C, {A} symmetric, row major (symmetric, so no swap needed for
    # {A} itself; the product is not symmetric, so the swap trick still applies overall)
    sym = rng.random((n, n))
    sym = sym + sym.T
    rhs = rng.random((n, n + 1))
    expected_symm = sym @ rhs

    As = grid((n, n))
    numpy.asarray(As)[:, :] = sym
    Bs = grid((n, n + 1))
    numpy.asarray(Bs)[:, :] = rhs
    Cs = grid((n, n + 1))
    # C(m,n) = A(m,m) B(m,n) row major -> swap to C^T(n,m) = B^T(n,m) A^T(m,m); {A}
    # symmetric so A^T=A needs no separate handling beyond the side/shape swap
    getattr(cublas, suffix + "symm")(
        handle, cublas.SideMode.RIGHT, cublas.FillMode.LOWER, n + 1, n, 1.0, As, n, Bs, n + 1,
        0.0, Cs, n + 1)
    assert numpy.allclose(numpy.asarray(Cs), expected_symm, atol=tol)

    cublas.destroy(handle)

    # cusolver: cholesky and inverse of a symmetric positive definite matrix
    spd = L @ L.T + n * numpy.eye(n)

    Aspd = grid((n, n))
    numpy.asarray(Aspd)[:, :] = spd

    solver = cusolver.create()
    # UPPER on the way in gives back a row-major LOWER factor, the same swap trick as above
    lwork = getattr(cusolver, suffix + "potrf_buffer_size")(solver, cublas.FillMode.UPPER, n, Aspd, n)
    workspace = grid((max(lwork, 1),))
    info = pyre.grid.managed(shape=(1,), cell="int32")
    getattr(cusolver, suffix + "potrf")(
        solver, cublas.FillMode.UPPER, n, Aspd, n, workspace, lwork, info)

    factor = numpy.tril(numpy.asarray(Aspd))
    assert numpy.allclose(factor, numpy.linalg.cholesky(spd), atol=tol)

    lwork = getattr(cusolver, suffix + "potri_buffer_size")(solver, cublas.FillMode.UPPER, n, Aspd, n)
    workspace = grid((max(lwork, 1),))
    info = pyre.grid.managed(shape=(1,), cell="int32")
    getattr(cusolver, suffix + "potri")(
        solver, cublas.FillMode.UPPER, n, Aspd, n, workspace, lwork, info)

    # only the lower triangle of the inverse was written; mirror it before comparing
    inverse = numpy.asarray(Aspd).copy()
    upper = numpy.triu_indices(n, k=1)
    inverse[upper] = inverse[(upper[1], upper[0])]
    assert numpy.allclose(inverse, numpy.linalg.inv(spd), atol=max(tol, 1e-5))

    cusolver.destroy(solver)

    # curand: fill grids straight from a device generator
    curand = pyre.cuda.curand
    generator = curand.create_generator(curand.RngType.DEFAULT)
    curand.set_seed(generator, 2026)

    uniform_name = "generate_uniform_double" if precision == "float64" else "generate_uniform"
    normal_name = "generate_normal_double" if precision == "float64" else "generate_normal"

    uniform = grid((100,))
    getattr(curand, uniform_name)(generator, uniform, 100)
    values = numpy.asarray(uniform)
    assert values.min() >= 0.0 and values.max() <= 1.0

    normal = grid((10000,))
    getattr(curand, normal_name)(generator, normal, 10000, 0.0, 1.0)
    values = numpy.asarray(normal)
    assert abs(values.mean()) < 0.1
    assert abs(values.std() - 1.0) < 0.1

    curand.destroy_generator(generator)

    # all done
    return


def checkCachedHandles():
    """
    A simulation calls into cublas/cusolver/curand every step, so the device caches one
    handle/generator of each and hands back the same one every time, rather than paying for a
    fresh allocation on every call
    """
    import numpy
    import pyre.cuda
    import pyre.grid

    device = pyre.cuda.manager.devices[0]

    # the same handle comes back every time
    assert device.cublasHandle == device.cublasHandle
    assert device.cusolverHandle == device.cusolverHandle
    assert device.curandGenerator() == device.curandGenerator()

    # and it actually works
    x = pyre.grid.managed(shape=(4,), cell="float64")
    y = pyre.grid.managed(shape=(4,), cell="float64")
    numpy.asarray(x)[:] = [1.0, 2.0, 3.0, 4.0]
    numpy.asarray(y)[:] = 0.0
    pyre.cuda.cublas.daxpy(device.cublasHandle, 4, 2.0, x, 1, y, 1)
    assert numpy.allclose(numpy.asarray(y), [2.0, 4.0, 6.0, 8.0])

    # all done
    return


def test():
    # check both precisions altar cares about
    check("float64")
    check("float32")
    # the per-device handle cache
    checkCachedHandles()
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
