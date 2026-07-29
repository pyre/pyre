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
#include "AnyMosaic.h"


// assemble a type-erased mosaic from its layout and the closures that reach its storage
pyre::py::grid::AnyMosaic::AnyMosaic(
    packing_type packing, string_t cell, census_type residents, pane_maker_type pane,
    probe_type resident, probe_type valid, probe_type clean, mark_type validate, mark_type taint,
    mark_type flush, reader_type read, writer_type write) :
    // adopt the layout
    _packing { std::move(packing) },
    // the name of the cell type
    _cell { std::move(cell) },
    // the census
    _residents { std::move(residents) },
    // the pane maker
    _pane { std::move(pane) },
    // the page state probes
    _resident { std::move(resident) },
    _valid { std::move(valid) },
    _clean { std::move(clean) },
    // the page state marks
    _validate { std::move(validate) },
    _taint { std::move(taint) },
    _flush { std::move(flush) },
    // and the pair that moves a cell to and from python
    _read { std::move(read) },
    _write { std::move(write) }
{}


// accessors

// the extent along each axis
auto
pyre::py::grid::AnyMosaic::shape() const -> const shape_type &
{
    // the layout knows
    return _packing.shape();
}

// the smallest addressable index
auto
pyre::py::grid::AnyMosaic::origin() const -> const index_type &
{
    // the layout knows
    return _packing.origin();
}

// the number of axes
auto
pyre::py::grid::AnyMosaic::rank() const -> std::size_t
{
    // the layout knows
    return _packing.rank();
}

// the extent of the grid of tiles
auto
pyre::py::grid::AnyMosaic::tiles() const -> const shape_type &
{
    // the layout knows
    return _packing.tiles();
}

// the extent of one tile
auto
pyre::py::grid::AnyMosaic::tileShape() const -> const shape_type &
{
    // the layout knows
    return _packing.tileShape();
}

// the number of cells the storage supplies
auto
pyre::py::grid::AnyMosaic::cells() const -> size_type
{
    // every tile at full size, padding included
    return _packing.cells();
}

// the name of my cell type
auto
pyre::py::grid::AnyMosaic::cell() const -> const string_t &
{
    // hand out the name
    return _cell;
}

// the number of pages that are actually resident
auto
pyre::py::grid::AnyMosaic::residents() const -> size_type
{
    // ask the storage
    return _residents();
}


// tiling interface

// the coordinates, in the grid of tiles, of the tile a given index falls in
auto
pyre::py::grid::AnyMosaic::tileOf(const index_type & index) const -> index_type
{
    // the index must name one axis per rank
    if (index.size() != rank()) {
        // anything else is a caller mistake
        throw py::index_error("the index must have one coordinate per axis");
    }
    // go through the axes
    for (std::size_t axis = 0; axis < rank(); ++axis) {
        // the index must fall inside my box
        if (index[axis] < origin()[axis] || index[axis] >= origin()[axis] + shape()[axis]) {
            // otherwise reject it
            throw py::index_error("index out of range");
        }
    }
    // the layout knows
    return _packing.tileOf(index);
}

// the tiles a box with the given anchor and extent touches
auto
pyre::py::grid::AnyMosaic::tilesOverlapping(
    const index_type & base, const shape_type & extent) const -> std::vector<index_type>
{
    // the box must name one axis per rank
    if (base.size() != rank() || extent.size() != rank()) {
        // anything else is a caller mistake
        throw py::index_error("the box must have one coordinate and one extent per axis");
    }
    // go through the axes
    for (std::size_t axis = 0; axis < rank(); ++axis) {
        // the box must be at least one cell wide
        if (extent[axis] < 1) {
            // otherwise there is nothing to touch
            throw py::value_error("the box must be at least one cell wide along each axis");
        }
        // and it must fit inside mine
        if (base[axis] < origin()[axis]
            || base[axis] + extent[axis] > origin()[axis] + shape()[axis]) {
            // otherwise reject it
            throw py::index_error("the box reaches outside the mosaic");
        }
    }
    // ask the layout for the touched tiles, as a box in tile space
    auto touched = pyre::grid::tilesOverlapping(_packing, base, extent);
    // room for the answer
    std::vector<index_type> result;
    // it holds one set of coordinates per touched tile
    result.reserve(touched.cells());
    // go through the touched tiles
    for (const auto & t : touched) {
        // and collect each one
        result.push_back(t);
    }
    // hand off the working set
    return result;
}

// the pane over a tile
auto
pyre::py::grid::AnyMosaic::pane(const index_type & tile) const -> AnyGrid
{
    // guard the coordinates; the ordinal itself is recomputed by the maker, which addresses
    // the storage in its own concrete terms
    _ordinal(tile);
    // carve the pane, materializing the tile's page on first touch
    return _pane(tile);
}


// item access

// {m[i, j, ...]}: the cell at a full integer index
auto
pyre::py::grid::AnyMosaic::getitem(const py::object & key) const -> py::object
{
    // resolve the key into box coordinates
    auto index = _index(key);
    // the page that backs the cell
    auto ordinal = _packing.tileOrdinal(_packing.tileOf(index));
    // a cell on a page that was never brought in holds nothing meaningful
    if (!_resident(ordinal)) {
        // so reading it is a caller mistake; refuse, with an exception python can catch
        throw py::value_error("reading a cell on a page that is not resident");
    }
    // lift the cell into python
    return _read(index);
}

// {m[i, j, ...] = v}: write {v} into the cell at a full integer index
auto
pyre::py::grid::AnyMosaic::setitem(const py::object & key, const py::object & value) const -> void
{
    // resolve the key into box coordinates and deposit the value; the writer materializes the
    // page on first touch and taints it, since the divergence is visible from here
    return _write(_index(key), value);
}


// page state

// whether a tile's page has been allocated
auto
pyre::py::grid::AnyMosaic::resident(const index_type & tile) const -> bool
{
    // fold the tile onto its page and probe it
    return _resident(_ordinal(tile));
}

// whether the client has deposited meaningful content in it
auto
pyre::py::grid::AnyMosaic::valid(const index_type & tile) const -> bool
{
    // fold the tile onto its page and probe it
    return _valid(_ordinal(tile));
}

// whether its content matches the client's backing store
auto
pyre::py::grid::AnyMosaic::clean(const index_type & tile) const -> bool
{
    // fold the tile onto its page and probe it
    return _clean(_ordinal(tile));
}

// record that the client has deposited meaningful content in a tile's page
auto
pyre::py::grid::AnyMosaic::validate(const index_type & tile) const -> void
{
    // fold the tile onto its page and mark it
    return _validate(_ordinal(tile));
}

// record that the client has written to a tile's page
auto
pyre::py::grid::AnyMosaic::taint(const index_type & tile) const -> void
{
    // fold the tile onto its page and mark it
    return _taint(_ordinal(tile));
}

// record that the client has saved a tile's page
auto
pyre::py::grid::AnyMosaic::flush(const index_type & tile) const -> void
{
    // fold the tile onto its page and mark it
    return _flush(_ordinal(tile));
}


// implementation details

// guard tile coordinates and fold them to the ordinal of the page that backs the tile
auto
pyre::py::grid::AnyMosaic::_ordinal(const index_type & tile) const -> size_type
{
    // the coordinates must name one axis per rank
    if (tile.size() != rank()) {
        // anything else is a caller mistake
        throw py::index_error("the tile must have one coordinate per axis");
    }
    // go through the axes
    for (std::size_t axis = 0; axis < rank(); ++axis) {
        // the coordinates must fall inside the tile grid
        if (tile[axis] < 0 || tile[axis] >= tiles()[axis]) {
            // otherwise reject them
            throw py::index_error("tile out of range");
        }
    }
    // the layout knows how the tiles are numbered
    return _packing.tileOrdinal(tile);
}

// resolve a python key into box coordinates
auto
pyre::py::grid::AnyMosaic::_index(const py::object & key) const -> index_type
{
    // room for the answer
    index_type index;
    // a tuple supplies one coordinate per axis
    if (py::isinstance<py::tuple>(key)) {
        // go through its items
        for (const auto & item : key.cast<py::tuple>()) {
            // and adopt each one as a coordinate
            index.push_back(item.cast<size_type>());
        }
    } else {
        // anything else must be a lone integer, which addresses a one dimensional mosaic
        index.push_back(key.cast<size_type>());
    }
    // the key must name one coordinate per axis
    if (index.size() != rank()) {
        // anything else is a caller mistake
        throw py::index_error("the index must have one coordinate per axis");
    }
    // go through the axes
    for (std::size_t axis = 0; axis < rank(); ++axis) {
        // a coordinate below the origin counts back from the end of its axis
        if (index[axis] < origin()[axis]) {
            // so wrap it around
            index[axis] += origin()[axis] + shape()[axis];
        }
        // by now, the coordinate must fall inside my box
        if (index[axis] < origin()[axis] || index[axis] >= origin()[axis] + shape()[axis]) {
            // otherwise reject it
            throw py::index_error("index out of range");
        }
    }
    // hand off the coordinates
    return index;
}


// end of file
