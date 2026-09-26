// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "externals.h"
// forward declarations
#include "forward.h"
// the type-erased grid
#include "AnyGrid.h"
// the vocabulary of in-place arithmetic
#include "arithmetic.h"


// the translation of python operands into the terms of in-place arithmetic
namespace pyre::py::grid::inplace {
    // the arithmetic cell type of a buffer protocol {format}
    inline auto cell(string_t format) -> arithmetic::Cell;

    // the layout of the block of cells a buffer protocol description, {info}, describes
    inline auto layout(const py::buffer_info & info) -> arithmetic::Layout;

    // whether {a} and {b} reach some of the same cells, of width {itemsize}, without being the
    // same view of them
    inline auto overlap(
        const arithmetic::Layout & a, const arithmetic::Layout & b, std::int64_t itemsize) -> bool;

    // the range of values integer cells of type {cell} hold
    inline auto bounds(arithmetic::Cell cell) -> std::pair<py::int_, py::int_>;

    // translate the python number {value} for a target with cells of type {cell} into {result};
    // {false} when {value} is not a number
    inline auto scalar(const py::handle & value, arithmetic::Cell cell, arithmetic::Scalar & result)
        -> bool;

    // {self op= other}, with {engineT} doing the work; {other} is a grid of the same shape and
    // cell type, any buffer when the engine reaches host memory, or a python number; anything
    // else is left for python to refuse
    template <class engineT>
    auto apply(py::object self, py::object other, arithmetic::Operation op) -> py::object;
} // namespace pyre::py::grid::inplace


// the inline implementations
#include "inplace.icc"


// end of file
