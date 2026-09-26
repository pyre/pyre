#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

"""
pyre.grid with nvmath-python: two ways in

  1. the high-level api ({nvmath.linalg.advanced}, {nvmath.fft}) recognizes numpy, cupy, and
     torch operands only, so a grid goes in through its numpy view; nvmath sees host memory,
     stages the operands to the device and back, and returns a fresh numpy array
  2. the low-level bindings ({nvmath.bindings.cublas}, {nvmath.bindings.cusolverDn}) take raw
     pointers, so a grid on managed memory goes in through {grid.address}; no copies, and the
     results land in the grid itself

cublas and cusolver are column major: a row-major grid read as column major is its transpose,
so row-major callers swap operands (C^T = B^T A^T) and ask for the opposite triangle

needs pyre built {WITH_CUDA}, and nvmath-python; the plain {nvmath-python} wheel uses the cuda
toolkit already installed, while the {[cu13]} extra would pull the math libraries in as wheels
"""

import numpy
import pyre.grid
import nvmath.fft
import nvmath.linalg.advanced
from cuda.bindings import runtime as cudart
from nvmath.bindings import cublas, cusolverDn


def managed(shape, cell="float64"):
    """A fresh grid on managed memory"""
    return pyre.grid.managed(shape=shape, cell=cell)


def sync():
    """Wait for the device, so the host can read managed memory"""
    (status,) = cudart.cudaDeviceSynchronize()
    assert status == cudart.cudaError_t.cudaSuccess, status


def highlevel(rng):
    """The high-level api, over numpy views of grids"""
    m, k, n = 64, 48, 32
    a, b = managed((m, k)), managed((k, n))
    numpy.asarray(a)[...] = rng.random((m, k))
    numpy.asarray(b)[...] = rng.random((k, n))

    # matmul: the product comes back as a new numpy array
    c = nvmath.linalg.advanced.matmul(numpy.asarray(a), numpy.asarray(b))
    error = numpy.abs(c - numpy.asarray(a) @ numpy.asarray(b)).max()
    print(f"matmul       {type(c).__name__}{c.shape}: max error {error:.3e}")

    # fft: likewise, except that for host operands it defaults to running on the cpu, which
    # needs mkl; ask for the device explicitly
    signal = managed((1024,), cell="complex128")
    numpy.asarray(signal)[...] = rng.random(1024) + 1j * rng.random(1024)
    spectrum = nvmath.fft.fft(numpy.asarray(signal), execution="cuda")
    error = numpy.abs(spectrum - numpy.fft.fft(numpy.asarray(signal))).max()
    print(f"fft          {type(spectrum).__name__}{spectrum.shape}: max error {error:.3e}")


def gemm(handle, a, b, c):
    """c = a b for row-major grids, in place, through cublas"""
    m, k = a.shape
    _, n = b.shape
    # cublas reads its scalars from host memory by default
    alpha, beta = numpy.array([1.0]), numpy.array([0.0])
    # row-major c = a b is column-major c^T = b^T a^T
    cublas.dgemm(handle, cublas.Operation.N, cublas.Operation.N, n, m, k,
                 alpha.ctypes.data, b.address, n, a.address, k,
                 beta.ctypes.data, c.address, n)
    sync()
    return c


def cholesky(handle, s):
    """The lower cholesky factor of a row-major symmetric positive definite grid, in place"""
    n, _ = s.shape
    # row-major lower is column-major upper
    uplo = cublas.FillMode.UPPER
    # cusolver wants a workspace and a status flag on the device; grids serve for both
    lwork = cusolverDn.dpotrf_buffer_size(handle, uplo, n, s.address, n)
    work = managed((max(lwork, 1),))
    info = managed((1,), cell="int32")
    cusolverDn.dpotrf(handle, uplo, n, s.address, n, work.address, lwork, info.address)
    sync()
    assert info[0] == 0, f"dpotrf: info = {info[0]}"
    # only the lower triangle holds the factor
    return numpy.tril(numpy.asarray(s))


def lowlevel(rng):
    """The low-level bindings, over grid addresses"""
    blas = cublas.create()
    solver = cusolverDn.create()

    # gemm into a grid
    m, k, n = 64, 48, 32
    a, b, c = managed((m, k)), managed((k, n)), managed((m, n))
    numpy.asarray(a)[...] = rng.random((m, k))
    numpy.asarray(b)[...] = rng.random((k, n))
    gemm(blas, a, b, c)
    error = numpy.abs(numpy.asarray(c) - numpy.asarray(a) @ numpy.asarray(b)).max()
    print(f"cublas.dgemm grid{c.shape} {c.strategy}: max error {error:.3e}")

    # cholesky of a grid, in place
    n = 256
    x = rng.random((n, n))
    spd = x @ x.T + n * numpy.eye(n)
    s = managed((n, n))
    numpy.asarray(s)[...] = spd
    lower = cholesky(solver, s)
    error = numpy.abs(lower @ lower.T - spd).max()
    print(f"dpotrf       grid{s.shape} {s.strategy}: max error |L L^T - S| {error:.3e}")

    cusolverDn.destroy(solver)
    cublas.destroy(blas)


def main():
    rng = numpy.random.default_rng(0)
    print("high-level api, through numpy views (staged copies):")
    highlevel(rng)
    print("low-level bindings, through grid.address (zero copy):")
    lowlevel(rng)


if __name__ == "__main__":
    main()


# end of file
