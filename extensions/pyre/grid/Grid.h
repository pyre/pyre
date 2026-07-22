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
    // reads the cell at an address and lifts it to a python object; built where the cell type is
    // still known, so the erased grid never has to parse its own format string
    using reader_type = std::function<py::object(const void *)>;
    // writes a python object into the cell at an address; the companion of {reader_type}
    using writer_type = std::function<void(void *, const py::object &)>;

    // metamethods
public:
    // assemble one directly; the {owner} is whatever must stay alive to keep {data} valid, and
    // {read}/{write} know how to move one cell between memory and python
    Grid(
        void * data, std::size_t itemsize, string_t format, std::vector<size_type> shape,
        std::vector<size_type> strides, bool writable, string_t strategy,
        std::shared_ptr<void> owner, reader_type read, writer_type write);

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

    // item access
public:
    // {g[i, j, ...]}: a full integer index yields the cell there; any slice, or fewer indices
    // than my rank, yields a sub-grid that shares my cells
    auto getitem(const py::object & key) const -> py::object;
    // {g[i, j, ...] = v}: write {v} into the cell at a full integer index
    auto setitem(const py::object & key, const py::object & value) -> void;

    // implementation details
private:
    // the outcome of reading a python index against my layout: the linear cell offset it lands
    // on, the residual extents and strides once integer axes are dropped and slices applied, and
    // whether every axis was pinned to a single cell
    struct resolved {
        size_type offset;
        std::vector<size_type> shape;
        std::vector<size_type> strides;
        bool scalar;
    };
    // turn a python index into the offset and residual layout it selects
    auto resolve(const py::object & key) const -> resolved;

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
    // lifts one cell from memory into python
    reader_type _read;
    // deposits one cell from python into memory
    writer_type _write;
};


// turn any statically typed grid into the erased form
// this is the demand-driven half of the design: it instantiates once per grid type that a bound
// signature actually mentions, not once per point of a precomputed cross product
namespace pyre::py::grid {
    // the low-level builder: describe {grid} in the buffer protocol's terms, over the block at
    // {data}, which {owner} is responsible for keeping alive; {strategy} names the storage kind
    template <class gridT>
    auto describe(const gridT & grid, string_t strategy, void * data, std::shared_ptr<void> owner)
        -> Grid;

    // erase a grid whose storage OWNS its cells (heap, map): keep a copy of the grid alive, so
    // that its storage's shared handle holds the block for as long as python holds on
    template <class gridT>
    auto erase(const gridT & grid, string_t strategy) -> Grid;
} // namespace pyre::py::grid


// the inline implementations
#include "Grid.icc"


// end of file
