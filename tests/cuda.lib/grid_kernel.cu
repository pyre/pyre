// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// the cuda runtime
#include <cuda_runtime.h>
// the grids over cuda storage
#include <pyre/cuda/grid.h>


// the layout
using pack_t = pyre::grid::canonical_t<2>;
// a grid on managed memory
using grid_t = pyre::cuda::grid::managed_t<pack_t, double>;
// and a view of its cells, for kernels
using view_t = pyre::cuda::grid::view_t<pack_t, double>;


// cell {i, j} gets {i + j}, through a view
__global__ void
fill(view_t view)
{
    // the extents
    const auto shape = view.packing().shape();
    // my row
    const int i = blockIdx.x;
    // and my column
    const int j = threadIdx.x;
    // if i am inside the grid
    if (i < shape[0] && j < shape[1]) {
        // set my cell
        view[{ i, j }] = i + j;
    }
    // all done
    return;
}


// every cell is doubled, through the grid that owns them
__global__ void
scale(grid_t grid)
{
    // my cell
    const int k = blockIdx.x * blockDim.x + threadIdx.x;
    // if it is inside the grid
    if (k < grid.packing().cells()) {
        // double it
        grid[k] *= 2;
    }
    // all done
    return;
}


// a managed grid, and a view of its cells, are indexed in kernels
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_kernel");

    // the shape
    const int rows = 8;
    const int cols = 16;
    // the layout
    pack_t packing { { rows, cols } };
    // a grid on managed memory
    grid_t grid { packing, packing.cells() };
    // and a view of its cells
    view_t view { grid.packing(), grid.storage().view() };

    // fill it on the device, through the view
    fill<<<rows, cols>>>(view);
    // double it on the device, through the grid itself
    scale<<<1, rows * cols>>>(grid);
    // wait for the device before the host reads the cells
    const auto status = cudaDeviceSynchronize();
    // the kernels ran
    assert(status == cudaSuccess);

    // go through the cells
    for (int i = 0; i < rows; ++i) {
        // all of them
        for (int j = 0; j < cols; ++j) {
            // each one holds what the kernels put there
            assert((grid[{ i, j }] == 2 * (i + j)));
        }
    }

    // all done
    return 0;
}


// end of file
