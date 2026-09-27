// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include <stdexcept>
#include <string>
#include <cuda_runtime.h>
#include <cuda/std/complex>
// my declarations
#include "engine.h"


// the kernels of in-place arithmetic on the device
namespace {
    // the arithmetic vocabulary
    namespace arithmetic = pyre::py::grid::arithmetic;

    // the number of threads in a block
    constexpr int threads = 256;

    // call {f} with the device type of the cells of type {cell}
    template <class functionT>
    auto withCell(arithmetic::Cell cell, functionT && f) -> void
    {
        // pick the cell type
        switch (cell) {
            // the signed integers
            case arithmetic::Cell::int8:
                return f.template operator()<std::int8_t>();
            case arithmetic::Cell::int16:
                return f.template operator()<std::int16_t>();
            case arithmetic::Cell::int32:
                return f.template operator()<std::int32_t>();
            case arithmetic::Cell::int64:
                return f.template operator()<std::int64_t>();
            // the unsigned integers
            case arithmetic::Cell::uint8:
                return f.template operator()<std::uint8_t>();
            case arithmetic::Cell::uint16:
                return f.template operator()<std::uint16_t>();
            case arithmetic::Cell::uint32:
                return f.template operator()<std::uint32_t>();
            case arithmetic::Cell::uint64:
                return f.template operator()<std::uint64_t>();
            // the floating point numbers
            case arithmetic::Cell::float32:
                return f.template operator()<float>();
            case arithmetic::Cell::float64:
                return f.template operator()<double>();
            // the complex numbers, laid out like the host ones
            case arithmetic::Cell::complex64:
                return f.template operator()<cuda::std::complex<float>>();
            case arithmetic::Cell::complex128:
                return f.template operator()<cuda::std::complex<double>>();
        }
        // all done
        return;
    }

    // combine the cells of {source} into the cells of {target}, striding over the cells
    template <arithmetic::Operation op, class cellT>
    __global__ void gridKernel(arithmetic::Layout target, arithmetic::Layout source)
    {
        // the cells of the target
        auto * a = static_cast<cellT *>(target.data);
        // and of the source
        const auto * b = static_cast<const cellT *>(source.data);
        // the distance between the cells a thread visits
        const auto stride = static_cast<std::int64_t>(gridDim.x) * blockDim.x;
        // visit the cells of this thread
        for (auto k = blockIdx.x * static_cast<std::int64_t>(blockDim.x) + threadIdx.x;
             k < target.cells; k += stride) {
            // and combine each pair
            arithmetic::apply<op>(
                a[arithmetic::offset(target, k)], b[arithmetic::offset(source, k)]);
        }
        // all done
        return;
    }

    // combine {value} into the cells of {target}, striding over the cells
    template <arithmetic::Operation op, class cellT>
    __global__ void scalarKernel(arithmetic::Layout target, cellT value)
    {
        // the cells of the target
        auto * a = static_cast<cellT *>(target.data);
        // the distance between the cells a thread visits
        const auto stride = static_cast<std::int64_t>(gridDim.x) * blockDim.x;
        // visit the cells of this thread
        for (auto k = blockIdx.x * static_cast<std::int64_t>(blockDim.x) + threadIdx.x;
             k < target.cells; k += stride) {
            // and combine each one with the value
            arithmetic::apply<op>(a[arithmetic::offset(target, k)], value);
        }
        // all done
        return;
    }

    // enough blocks to cover {cells}, capped so that larger grids stride instead
    auto blocks(std::int64_t cells) -> unsigned
    {
        // the blocks that cover the cells
        const auto needed = (cells + threads - 1) / threads;
        // but no more than the cap
        return static_cast<unsigned>(needed < 65535 ? needed : 65535);
    }

    // raise the failure to launch a kernel
    auto check(cudaError_t status) -> void
    {
        // if there is one
        if (status != cudaSuccess) {
            // say so
            throw std::runtime_error(std::string("pyre.cuda: ") + cudaGetErrorString(status));
        }
        // all done
        return;
    }
} // namespace


// combine the cells of {source} into the cells of {target}, on the device
auto
pyre::cuda::py::DeviceEngine::apply(
    operation_type op, cell_type cell, const layout_type & target, const layout_type & source)
    -> void
{
    // an empty grid has nothing to combine
    if (target.cells == 0) {
        // so leave it alone
        return;
    }
    // with the device type of the cells
    withCell(cell, [&]<class cellT>() {
        // and the operation fixed at compile time
        arithmetic::withOperation(op, [&](auto operation) {
            // launch the kernel, without waiting for it
            gridKernel<decltype(operation)::value, cellT>
                <<<blocks(target.cells), threads>>>(target, source);
        });
    });
    // raise a failure to launch; a failure while running surfaces when the host waits
    check(cudaGetLastError());
    // all done
    return;
}


// combine {value} into the cells of {target}, on the device
auto
pyre::cuda::py::DeviceEngine::apply(
    operation_type op, cell_type cell, const layout_type & target, const scalar_type & value)
    -> void
{
    // an empty grid has nothing to combine
    if (target.cells == 0) {
        // so leave it alone
        return;
    }
    // with the device type of the cells
    withCell(cell, [&]<class cellT>() {
        // and the operation fixed at compile time
        arithmetic::withOperation(op, [&](auto operation) {
            // launch the kernel, without waiting for it
            scalarKernel<decltype(operation)::value, cellT>
                <<<blocks(target.cells), threads>>>(target, arithmetic::value<cellT>(value));
        });
    });
    // raise a failure to launch; a failure while running surfaces when the host waits
    check(cudaGetLastError());
    // all done
    return;
}


// end of file
