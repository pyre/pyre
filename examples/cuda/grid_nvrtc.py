#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

"""
pyre.grid in cuda kernels, from python: a managed grid handed to a kernel compiled at runtime

NVRTC compiles device code only, without the host standard library pyre's headers need, so the
kernel gets what the grid publishes instead: its managed address, shape, and strides (in cells)

needs pyre built {WITH_CUDA}, and cuda-python's {cuda.core}
"""

import numpy
import pyre.grid
from cuda.core import Device, LaunchConfig, Program, ProgramOptions, launch

# y(i,j) = a x(i,j) + y(i,j), indexed through the strides the grid reports
SOURCE = r"""
extern "C" __global__ void
axpy2d(double a, const double * x, double * y, int rows, int cols, long si, long sj)
{
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    int j = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < rows && j < cols) {
        long k = i * si + j * sj;
        y[k] = a * x[k] + y[k];
    }
}
"""


def main():
    device = Device()
    device.set_current()
    stream = device.create_stream()

    # compile the kernel for this device
    arch = "".join(str(v) for v in device.compute_capability)
    program = Program(SOURCE, code_type="c++", options=ProgramOptions(arch=f"sm_{arch}"))
    kernel = program.compile("cubin").get_kernel("axpy2d")

    # two managed grids
    rows, cols = 300, 500
    x = pyre.grid.managed(shape=(rows, cols), cell="float64")
    y = pyre.grid.managed(shape=(rows, cols), cell="float64")
    # filled on the host through numpy views of the same cells; no copies
    rng = numpy.random.default_rng(0)
    numpy.asarray(x)[...] = rng.random((rows, cols))
    numpy.asarray(y)[...] = rng.random((rows, cols))
    expected = 2.5 * numpy.asarray(x) + numpy.asarray(y)

    # what the kernel needs from each grid: its address, plus the layout
    si, sj = y.strides
    config = LaunchConfig(grid=((cols + 31) // 32, (rows + 7) // 8), block=(32, 8))
    launch(stream, config, kernel,
           numpy.float64(2.5), x.address, y.address,
           numpy.int32(rows), numpy.int32(cols), numpy.int64(si), numpy.int64(sj))
    stream.sync()

    # the result is already in {y}; the host reads it in place
    print(f"grid {y.shape} {y.strategy}, strides {y.strides}, address {y.address:#x}")
    print(f"axpy2d: max error {numpy.abs(numpy.asarray(y) - expected).max():.3e}")

    # grids on cuda storage also speak the cuda array interface, so libraries that take it
    # (numba, cupy, cuda.core) can use them directly
    print(f"__cuda_array_interface__: {y.__cuda_array_interface__}")


if __name__ == "__main__":
    main()


# end of file
