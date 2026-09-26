// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once


// externals
#include <cstdint>


// in-place elementwise arithmetic on type-erased grids: {+=}, {-=}, {*=}, {/=}, with either a
// grid of the same shape and cell type or a scalar on the right
// the declarations here are plain c++, with no python in sight, so that the cuda half can be
// compiled by nvcc without dragging pybind11 along; the bindings translate python operands into
// these descriptions, and pick the half that matches where the target grid's cells live
namespace pyre::py::grid::arithmetic {
    // the operations
    enum class op_t : int { add, sub, mul, div };

    // the cell types the grid factories produce
    enum class cell_t : int {
        int8,
        int16,
        int32,
        int64,
        uint8,
        uint16,
        uint32,
        uint64,
        float32,
        float64,
        complex64,
        complex128,
    };

    // the most axes a layout can describe
    inline constexpr int maxRank = 16;

    // a strided block of cells: where it starts, its extents, and its strides, in cells
    struct layout_t {
        // the address of the first cell
        void * data;
        // the number of axes
        int rank;
        // the number of cells
        std::int64_t cells;
        // whether the cells are packed in row major order, so the flat index is the offset
        bool contiguous;
        // the extent along each axis
        std::int64_t shape[maxRank];
        // the distance between consecutive cells along each axis, in cells
        std::int64_t strides[maxRank];
    };

    // a scalar operand, in every spelling a cell type might want it in; the bindings fill in
    // the one that matches the target's cell type
    struct scalar_t {
        std::int64_t i;
        std::uint64_t u;
        double re;
        double im;
    };

    // on the host
    auto host(op_t, cell_t, const layout_t & self, const layout_t & other) -> void;
    auto host(op_t, cell_t, const layout_t & self, const scalar_t & other) -> void;

#ifdef WITH_CUDA
    // on the device; these launch on the default stream and return without waiting, so the
    // host must {synchronize} before it reads the cells
    auto device(op_t, cell_t, const layout_t & self, const layout_t & other) -> void;
    auto device(op_t, cell_t, const layout_t & self, const scalar_t & other) -> void;
    // wait for the device, and report any failure of the launches still in flight
    auto synchronize() -> void;
#endif
} // namespace pyre::py::grid::arithmetic


// end of file
