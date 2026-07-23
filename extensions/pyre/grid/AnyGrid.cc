// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// my declarations
#include "AnyGrid.h"


// assemble a type-erased grid from its parts
pyre::py::grid::AnyGrid::AnyGrid(
    void * data, std::size_t itemsize, string_t format, std::vector<size_type> shape,
    std::vector<size_type> strides, bool writable, string_t strategy, std::shared_ptr<void> owner,
    reader_type read, writer_type write) :
    // adopt the block
    _data { data },
    // its cell width
    _itemsize { itemsize },
    // its cell description
    _format { std::move(format) },
    // its shape
    _shape { std::move(shape) },
    // its strides, in cells
    _strides { std::move(strides) },
    // its mutability
    _writable { writable },
    // its storage kind
    _strategy { std::move(strategy) },
    // the handle that keeps it alive
    _owner { std::move(owner) },
    // and the pair that moves a cell to and from python
    _read { std::move(read) },
    _write { std::move(write) }
{}


// describe myself in the terms the python buffer protocol speaks
auto
pyre::py::grid::AnyGrid::view() -> py::buffer_info
{
    // the protocol wants strides in bytes, so scale my cell strides by the cell width
    std::vector<py::ssize_t> byteStrides;
    // one per axis
    for (auto s : _strides) {
        // from cells to bytes
        byteStrides.push_back(static_cast<py::ssize_t>(s) * static_cast<py::ssize_t>(_itemsize));
    }
    // the extents, in the protocol's own signed type
    std::vector<py::ssize_t> extents(_shape.begin(), _shape.end());
    // hand back the full description; {_writable} decides whether the buffer is read-only
    return py::buffer_info(
        _data, static_cast<py::ssize_t>(_itemsize), _format,
        static_cast<py::ssize_t>(_shape.size()), extents, byteStrides, !_writable);
}


// the extent along each axis
auto
pyre::py::grid::AnyGrid::shape() const -> const std::vector<size_type> &
{
    // hand out my extents
    return _shape;
}


// the distance between consecutive cells along each axis, in cells
auto
pyre::py::grid::AnyGrid::strides() const -> const std::vector<size_type> &
{
    // hand out my strides
    return _strides;
}


// the number of axes
auto
pyre::py::grid::AnyGrid::rank() const -> std::size_t
{
    // the length of my shape is my rank
    return _shape.size();
}


// whether python may write through to my cells
auto
pyre::py::grid::AnyGrid::writable() const -> bool
{
    // hand out my mutability
    return _writable;
}


// the storage strategy that holds my cells
auto
pyre::py::grid::AnyGrid::strategy() const -> const string_t &
{
    // hand out my storage kind
    return _strategy;
}


// turn a python index into the offset and residual layout it selects
auto
pyre::py::grid::AnyGrid::resolve(const py::object & key) const -> resolved
{
    // collect the per-axis indexers, however the key was spelled
    std::vector<py::object> items;
    // a tuple spreads across the leading axes
    if (py::isinstance<py::tuple>(key)) {
        // one entry per axis it mentions
        for (auto handle : py::cast<py::tuple>(key)) {
            items.push_back(py::reinterpret_borrow<py::object>(handle));
        }
    }
    // anything else indexes the first axis alone
    else {
        // a single indexer
        items.push_back(key);
    }
    // my rank bounds how many axes can be addressed
    const auto rank = _shape.size();
    // more indexers than axes is a mistake
    if (items.size() > rank) {
        // reject the excess
        throw py::index_error("too many indices for grid");
    }

    // accumulate the linear offset and the residual layout
    size_type offset = 0;
    // the extents and strides that survive
    std::vector<size_type> shape, strides;
    // until an axis escapes an integer, the index still names a single cell
    bool scalar = true;
    // walk every axis
    for (std::size_t axis = 0; axis < rank; ++axis) {
        // its extent
        const auto extent = _shape[axis];
        // and stride
        const auto stride = _strides[axis];
        // axes past the supplied indexers are taken whole
        if (axis >= items.size()) {
            // keep the axis intact
            shape.push_back(extent);
            strides.push_back(stride);
            // it is no longer a single cell
            scalar = false;
            // on to the next axis
            continue;
        }
        // the indexer for this axis
        const auto & item = items[axis];
        // a slice selects a strided run
        if (py::isinstance<py::slice>(item)) {
            // storage for the unpacked bounds
            py::ssize_t start = 0, stop = 0, step = 0, span = 0;
            // let pybind11 do the arithmetic, including negative bounds and steps
            if (!py::cast<py::slice>(item).compute(extent, &start, &stop, &step, &span)) {
                // it has already registered the right exception
                throw py::error_already_set();
            }
            // step to the first selected cell
            offset += static_cast<size_type>(start) * stride;
            // keep the axis, now the length of the run
            shape.push_back(static_cast<size_type>(span));
            // with a stride scaled by the slice step
            strides.push_back(stride * static_cast<size_type>(step));
            // a slice keeps the axis, so this is no longer a single cell
            scalar = false;
        }
        // otherwise treat it as an integer coordinate
        else {
            // read it out
            auto i = py::cast<size_type>(item);
            // fold a negative coordinate against the extent
            if (i < 0) {
                i += extent;
            }
            // reject anything still out of range
            if (i < 0 || i >= extent) {
                // out of bounds
                throw py::index_error("grid index out of range");
            }
            // pin this axis; it drops out of the residual layout
            offset += i * stride;
        }
    }
    // hand back the offset, the residual layout, and whether a single cell was named
    return { offset, std::move(shape), std::move(strides), scalar };
}


// {g[i, j, ...]}: a cell for a full index, a sub-grid for a partial or sliced one
auto
pyre::py::grid::AnyGrid::getitem(const py::object & key) const -> py::object
{
    // resolve the index against my layout
    const auto r = resolve(key);
    // the block address the offset lands on
    auto * cell = static_cast<char *>(_data) + r.offset * static_cast<size_type>(_itemsize);
    // a full integer index names one cell
    if (r.scalar) {
        // lift it into python
        return _read(cell);
    }
    // otherwise hand back a sub-grid that shares my cells and my keep-alive handle
    return py::cast(AnyGrid(
        // over the block the offset selected
        cell,
        // the same cell width
        _itemsize,
        // and description
        _format,
        // the residual extents
        r.shape,
        // and strides
        r.strides,
        // the same mutability
        _writable,
        // and storage kind
        _strategy,
        // pinned alive by the very handle i hold
        _owner,
        // moving cells the same way i do
        _read, _write));
}


// {g[i, j, ...] = v}: write {v} into the cell at a full integer index
auto
pyre::py::grid::AnyGrid::setitem(const py::object & key, const py::object & value) -> void
{
    // resolve the index against my layout
    const auto r = resolve(key);
    // only a full integer index, naming a single cell, may be assigned this way
    if (!r.scalar) {
        // a slice target would need array assignment; steer the caller to a view instead
        throw py::index_error(
            "only a full integer index may be assigned; index the sub-grid and write its cells");
    }
    // refuse to write through a read-only grid
    if (!_writable) {
        // say so plainly
        throw py::value_error("this grid is read-only");
    }
    // the block address the offset lands on
    auto * cell = static_cast<char *>(_data) + r.offset * static_cast<size_type>(_itemsize);
    // deposit the value
    _write(cell, value);
}


// end of file
