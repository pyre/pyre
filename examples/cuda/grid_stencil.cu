// -*- C++ -*-
// -*- coding: utf-8 -*-

// pyre::grid in cuda kernels: a 5-point laplacian over managed memory
//
// build against a pyre installed with {WITH_CUDA} under {PREFIX}:
//   nvcc -std=c++20 -arch=native --expt-relaxed-constexpr -DWITH_CUDA \
//        -I$PREFIX/include -L$PREFIX/lib -Xlinker -rpath=$PREFIX/lib \
//        -lpyre -ljournal -lpyrecuda -o grid_stencil grid_stencil.cu
//
// {--expt-relaxed-constexpr} lets device code use the constexpr std::array machinery under
// pyre's indices and shapes; {-DWITH_CUDA} turns on the {PYRE_HOST_DEVICE} decorations

#include <cmath>
#include <cstdio>
#include <cuda_runtime.h>

#include <pyre/grid.h>
#include <pyre/cuda/memory.h>

// a 2d row-major layout over managed memory: the host allocates it, owns it, and reads it;
// kernels take it by value and index it exactly the way the host does
using pack_t = pyre::grid::canonical_t<2>;
using grid_t = pyre::grid::grid_t<pack_t, pyre::cuda::memory::managed_t<double>>;
// the same cells without the ownership: trivially copyable, for kernels that shouldn't carry
// the host's shared_ptr around
using view_t = pyre::grid::grid_t<pack_t, pyre::memory::View<double, false>>;

// lap(i,j) = u(i-1,j) + u(i+1,j) + u(i,j-1) + u(i,j+1) - 4 u(i,j), on the interior
__global__ void
laplacian(grid_t u, grid_t lap, double h)
{
    // the extents travel with the grid
    auto shape = u.packing().shape();
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    int j = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < 1 || j < 1 || i >= shape[0] - 1 || j >= shape[1] - 1) {
        return;
    }
    lap[{ i, j }] = (u[{ i - 1, j }] + u[{ i + 1, j }] + u[{ i, j - 1 }] + u[{ i, j + 1 }]
                     - 4 * u[{ i, j }])
                  / (h * h);
}

// flat traversal over a view: offsets, with the packing recovering the index when needed
__global__ void
zero_boundary(view_t g)
{
    auto shape = g.packing().shape();
    int k = blockIdx.x * blockDim.x + threadIdx.x;
    if (k >= g.packing().cells()) {
        return;
    }
    auto idx = g.packing()[k];
    if (idx[0] == 0 || idx[1] == 0 || idx[0] == shape[0] - 1 || idx[1] == shape[1] - 1) {
        g[k] = 0;
    }
}

int
main()
{
    const int n = 256;
    const double h = 1.0 / (n - 1);

    // two grids on managed memory
    pack_t packing { { n, n } };
    grid_t u { packing, packing.cells() };
    grid_t lap { packing, packing.cells() };

    // fill u(x,y) = x^2 + y^2 on the host, through the same index operator the kernel uses;
    // its laplacian is exactly 4, which the 5-point stencil reproduces up to roundoff
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            double x = i * h, y = j * h;
            u[{ i, j }] = x * x + y * y;
        }

    // the owning grids go straight into the kernel
    dim3 block(32, 8);
    dim3 blocks((n + block.x - 1) / block.x, (n + block.y - 1) / block.y);
    laplacian<<<blocks, block>>>(u, lap, h);
    // a view of {lap} for the second pass
    zero_boundary<<<(n * n + 255) / 256, 256>>>(view_t { lap.packing(), lap.storage().view() });
    // managed memory: synchronize, then the host reads the results in place
    cudaDeviceSynchronize();

    // check on the host
    double worst = 0;
    for (int i = 1; i < n - 1; ++i)
        for (int j = 1; j < n - 1; ++j) worst = std::fmax(worst, std::fabs(lap[{ i, j }] - 4.0));
    double edge = lap[{ 0, n / 2 }] + lap[{ n - 1, n / 2 }] + lap[{ n / 2, 0 }] + lap[{ n / 2, n - 1 }];
    std::printf("interior: max |lap u - 4| = %.3e\n", worst);
    std::printf("boundary: sum of sampled edge cells = %g\n", edge);
    return 0;
}


// end of file
