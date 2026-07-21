// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"
// forward declarations
#include "forward.h"


// the erased grid that the bindings expose to python
// every c++ grid, whatever its rank, cell type, or storage strategy, collapses to one of these,
// so python sees a single class rather than a cross product of template instantiations
// it carries exactly what the python buffer protocol needs, plus a handle that keeps the cells
// alive for as long as python holds on
class pyre::py::grid::Grid {
    // types
public:
    // the signed integer type the grid measures extents and offsets with
    using size_type = std::ptrdiff_t;

    // metamethods
public:
    // assemble one directly; the {owner} is whatever must stay alive to keep {data} valid
    Grid(
        void * data, std::size_t itemsize, string_t format, std::vector<size_type> shape,
        std::vector<size_type> strides, bool writable, string_t strategy,
        std::shared_ptr<void> owner);

    // accessors
public:
    // the buffer protocol description numpy and friends consume
    auto view() -> py::buffer_info;
    // the extent along each axis
    auto shape() const -> const std::vector<size_type> &;
    // the distance between consecutive cells along each axis, in cells
    auto strides() const -> const std::vector<size_type> &;
    // the number of axes
    auto rank() const -> std::size_t;
    // whether python may write through to the cells
    auto writable() const -> bool;
    // which storage strategy backs me, kept for clients that care how my cells are held
    auto strategy() const -> const string_t &;

    // implementation details
private:
    // the address of my first cell
    void * _data;
    // how wide one cell is, in bytes
    std::size_t _itemsize;
    // the struct-module code that says how to read a cell
    string_t _format;
    // my extent along each axis
    std::vector<size_type> _shape;
    // my strides, in cells
    std::vector<size_type> _strides;
    // whether my cells may be written
    bool _writable;
    // the storage strategy that holds my cells
    string_t _strategy;
    // the handle that keeps my cells alive; usually a copy of the source grid, so that its
    // storage's shared reference count stays above zero for as long as i live
    std::shared_ptr<void> _owner;
};


// turn any statically typed grid into the erased form
// this is the demand-driven half of the design: it instantiates once per grid type that a bound
// signature actually mentions, not once per point of a precomputed cross product
namespace pyre::py::grid {
    // {strategy} names the storage kind, e.g. "heap"; {gridT} must compose a strided packing with
    // contiguous storage, which is what lets the buffer protocol describe it
    template <class gridT>
    auto erase(const gridT & grid, string_t strategy) -> Grid;
}


// the inline implementations
#include "Grid.icc"


// end of file
