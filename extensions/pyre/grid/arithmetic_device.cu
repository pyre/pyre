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
// the shared engine
#include "arithmetic.icc"


// the device half of the elementwise engine
namespace pyre::py::grid::arithmetic {
    namespace {
        // call {f} with the device type of a cell; complex cells are {cuda::std::complex},
        // which is laid out exactly like the host's {std::complex}
        template <class F>
        inline auto
        withCell(cell_t cell, F && f) -> void
        {
            switch (cell) {
                case cell_t::int8:
                    return f.template operator()<std::int8_t>();
                case cell_t::int16:
                    return f.template operator()<std::int16_t>();
                case cell_t::int32:
                    return f.template operator()<std::int32_t>();
                case cell_t::int64:
                    return f.template operator()<std::int64_t>();
                case cell_t::uint8:
                    return f.template operator()<std::uint8_t>();
                case cell_t::uint16:
                    return f.template operator()<std::uint16_t>();
                case cell_t::uint32:
                    return f.template operator()<std::uint32_t>();
                case cell_t::uint64:
                    return f.template operator()<std::uint64_t>();
                case cell_t::float32:
                    return f.template operator()<float>();
                case cell_t::float64:
                    return f.template operator()<double>();
                case cell_t::complex64:
                    return f.template operator()<cuda::std::complex<float>>();
                case cell_t::complex128:
                    return f.template operator()<cuda::std::complex<double>>();
            }
            throw std::logic_error("arithmetic: unknown cell type");
        }

        // {self op= other}, one thread per cell, striding over the grid
        template <op_t op, class T>
        __global__ void
        gridKernel(layout_t self, layout_t other)
        {
            auto * a = static_cast<T *>(self.data);
            auto * b = static_cast<const T *>(other.data);
            auto stride = static_cast<std::int64_t>(gridDim.x) * blockDim.x;
            for (std::int64_t k = blockIdx.x * static_cast<std::int64_t>(blockDim.x) + threadIdx.x;
                 k < self.cells; k += stride) {
                apply<op>(a[offset(self, k)], b[offset(other, k)]);
            }
        }

        // {self op= scalar}, likewise
        template <op_t op, class T>
        __global__ void
        scalarKernel(layout_t self, T b)
        {
            auto * a = static_cast<T *>(self.data);
            auto stride = static_cast<std::int64_t>(gridDim.x) * blockDim.x;
            for (std::int64_t k = blockIdx.x * static_cast<std::int64_t>(blockDim.x) + threadIdx.x;
                 k < self.cells; k += stride) {
                apply<op>(a[offset(self, k)], b);
            }
        }

        // enough blocks to cover the grid, capped so large grids stride instead
        inline auto
        blocks(std::int64_t cells, int threads) -> unsigned
        {
            auto needed = (cells + threads - 1) / threads;
            return static_cast<unsigned>(needed < 65535 ? needed : 65535);
        }

        // turn a failed launch into an exception
        inline auto
        check(cudaError_t status, const char * what) -> void
        {
            if (status != cudaSuccess) {
                throw std::runtime_error(std::string(what) + ": " + cudaGetErrorString(status));
            }
        }

        // the block size
        constexpr int threads = 256;
    } // namespace


    // {self op= other}
    auto
    device(op_t op, cell_t cell, const layout_t & self, const layout_t & other) -> void
    {
        // nothing to do for an empty grid
        if (self.cells == 0) {
            return;
        }
        withCell(cell, [&]<class T>() {
            withOp(op, [&](auto tag) {
                gridKernel<decltype(tag)::value, T>
                    <<<blocks(self.cells, threads), threads>>>(self, other);
            });
        });
        // report a failure to launch; failures while running surface at {synchronize}
        check(cudaGetLastError(), "grid arithmetic");
    }


    // {self op= scalar}
    auto
    device(op_t op, cell_t cell, const layout_t & self, const scalar_t & other) -> void
    {
        // nothing to do for an empty grid
        if (self.cells == 0) {
            return;
        }
        withCell(cell, [&]<class T>() {
            withOp(op, [&](auto tag) {
                scalarKernel<decltype(tag)::value, T>
                    <<<blocks(self.cells, threads), threads>>>(self, value<T>(other));
            });
        });
        // report a failure to launch; failures while running surface at {synchronize}
        check(cudaGetLastError(), "grid arithmetic");
    }


    // wait for the device
    auto
    synchronize() -> void
    {
        check(cudaDeviceSynchronize(), "synchronize");
    }
} // namespace pyre::py::grid::arithmetic


// end of file
