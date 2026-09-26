// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <cstdint>
#include <type_traits>
#include <utility>
// the marks for the functions device code may call
#include <pyre/memory.h>


// the vocabulary of in-place arithmetic on type-erased grids, and the work it does on each
// cell; it has no python in it, so the code that runs on a device can use it too
namespace pyre::py::grid::arithmetic {
    // the operations
    enum class Operation : int { add, sub, mul, div };

    // the cell types the grid factories make
    enum class Cell : int {
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

    // a strided block of cells
    struct Layout {
        // the address of the first cell
        void * data;
        // the number of axes
        int rank;
        // the number of cells
        std::int64_t cells;
        // whether the cells are packed in row major order, so a flat index is an offset
        bool contiguous;
        // the extent along each axis
        std::int64_t shape[maxRank];
        // the distance between consecutive cells along each axis, in cells
        std::int64_t strides[maxRank];
    };

    // a scalar operand, in every spelling a cell type might want it in
    struct Scalar {
        // for signed integer cells
        std::int64_t i;
        // for unsigned integer cells
        std::uint64_t u;
        // the real part, for floating point and complex cells
        double re;
        // the imaginary part, for complex cells
        double im;
    };

    // the offset of the cell at row major position {k} of a {layout}
    PYRE_HOST_DEVICE inline auto offset(const Layout & layout, std::int64_t k) -> std::int64_t;

    // combine the cell {b} into the cell {a}
    template <Operation op, class cellT>
    PYRE_HOST_DEVICE inline auto apply(cellT & a, const cellT & b) -> void;

    // the {scalar} operand, as a {cellT}
    template <class cellT>
    PYRE_HOST_DEVICE inline auto value(const Scalar & scalar) -> cellT;

    // call {f} with the operation {op} as a compile time constant
    template <class functionT>
    inline auto withOperation(Operation op, functionT && f) -> void;
} // namespace pyre::py::grid::arithmetic


// the inline implementations
#include "arithmetic.icc"


// end of file
