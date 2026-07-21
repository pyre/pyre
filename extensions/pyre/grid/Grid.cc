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
#include "Grid.h"


// assemble an erased grid from its parts
pyre::py::grid::Grid::Grid(
    void * data, std::size_t itemsize, string_t format, std::vector<size_type> shape,
    std::vector<size_type> strides, bool writable, string_t strategy, std::shared_ptr<void> owner) :
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
    // and the handle that keeps it alive
    _owner { std::move(owner) }
{}


// describe myself in the terms the python buffer protocol speaks
auto
pyre::py::grid::Grid::view() -> py::buffer_info
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
pyre::py::grid::Grid::shape() const -> const std::vector<size_type> &
{
    // hand out my extents
    return _shape;
}


// the distance between consecutive cells along each axis, in cells
auto
pyre::py::grid::Grid::strides() const -> const std::vector<size_type> &
{
    // hand out my strides
    return _strides;
}


// the number of axes
auto
pyre::py::grid::Grid::rank() const -> std::size_t
{
    // the length of my shape is my rank
    return _shape.size();
}


// whether python may write through to my cells
auto
pyre::py::grid::Grid::writable() const -> bool
{
    // hand out my mutability
    return _writable;
}


// the storage strategy that holds my cells
auto
pyre::py::grid::Grid::strategy() const -> const string_t &
{
    // hand out my storage kind
    return _strategy;
}


// end of file
