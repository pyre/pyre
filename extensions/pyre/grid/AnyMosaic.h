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
// panes travel to python as type-erased grids
#include "AnyGrid.h"


// the type-erased mosaic the bindings expose to python
// a mosaic is a chunked packing married to paged storage: an out-of-core grid whose cells live
// on demand-materialized pages, one per tile, so there is no single block for the buffer
// protocol to describe; instead, python reaches the cells tile by tile, through panes: dense
// zero-copy grids over one page each
// only the cell type is erased: the runtime-rank packing is a concrete class, so it travels
// as itself, and everything that touches the storage is a closure built where the cell type
// is still known
class pyre::py::grid::AnyMosaic {
    // types
public:
    // the signed integer type the mosaic measures extents and offsets with
    using size_type = std::ptrdiff_t;
    // the runtime-rank tiled layout; concrete, so it needs no erasure
    using packing_type = pyre::grid::dynamic_chunked_t;
    // the containers it addresses with
    using index_type = packing_type::index_type;
    using shape_type = packing_type::shape_type;
    // carves the zero-copy pane over one tile; built where the cell type is still known, and
    // responsible for materializing the tile's page and pinning the store
    using pane_maker_type = std::function<AnyGrid(const index_type &)>;
    // counts the resident pages
    using census_type = std::function<size_type()>;
    // reads one of a page's state bits
    using probe_type = std::function<bool(size_type)>;
    // flips one of a page's state bits
    using mark_type = std::function<void(size_type)>;
    // lifts the cell at an index into python; built where the cell type is still known
    using reader_type = std::function<py::object(const index_type &)>;
    // deposits a python value into the cell at an index, materializing and tainting the page
    // that holds it; the companion of {reader_type}
    using writer_type = std::function<void(const index_type &, const py::object &)>;

    // metamethods
public:
    // assemble one from the layout and the closures that reach the storage
    AnyMosaic(
        packing_type packing, string_t cell, census_type residents, pane_maker_type pane,
        probe_type resident, probe_type valid, probe_type clean, mark_type validate,
        mark_type taint, mark_type flush, mark_type release, reader_type read, writer_type write);

    // accessors
public:
    // the extent along each axis
    auto shape() const -> const shape_type &;
    // the smallest addressable index
    auto origin() const -> const index_type &;
    // the number of axes
    auto rank() const -> std::size_t;
    // the extent of the grid of tiles
    auto tiles() const -> const shape_type &;
    // the extent of one tile
    auto tileShape() const -> const shape_type &;
    // the number of cells the storage supplies: every tile at full size, padding included
    auto cells() const -> size_type;
    // the name of my cell type, so python can build matching consumers
    auto cell() const -> const string_t &;
    // the number of pages that are actually resident
    auto residents() const -> size_type;

    // tiling interface
public:
    // the coordinates, in the grid of tiles, of the tile a given index falls in
    auto tileOf(const index_type & index) const -> index_type;
    // the tiles a box with the given anchor and extent touches, one set of coordinates each
    auto tilesOverlapping(const index_type & base, const shape_type & extent) const
        -> std::vector<index_type>;
    // the pane over a tile: a dense zero-copy grid over the page that holds it, materializing
    // the page on first touch
    auto pane(const index_type & tile) const -> AnyGrid;

    // item access
public:
    // {m[i, j, ...]}: the cell at a full integer index; reading a cell whose page was never
    // brought in is refused, since its content would be meaningless
    auto getitem(const py::object & key) const -> py::object;
    // {m[i, j, ...] = v}: write {v} into the cell at a full integer index, materializing the
    // page on first touch and tainting it, since the write is a divergence this binding can see
    auto setitem(const py::object & key, const py::object & value) const -> void;

    // page state
public:
    // whether a tile's page has been allocated
    auto resident(const index_type & tile) const -> bool;
    // whether the client has deposited meaningful content in it
    auto valid(const index_type & tile) const -> bool;
    // whether its content matches the client's backing store
    auto clean(const index_type & tile) const -> bool;
    // record that the client has deposited meaningful content in a tile's page
    auto validate(const index_type & tile) const -> void;
    // record that the client has written to a tile's page
    auto taint(const index_type & tile) const -> void;
    // record that the client has saved a tile's page
    auto flush(const index_type & tile) const -> void;
    // let go of a tile's page, returning it to the never-touched state; outstanding panes
    // keep their block, but no longer alias the mosaic's cells
    auto release(const index_type & tile) const -> void;

    // implementation details
private:
    // guard tile coordinates, complaining when they reach outside the tile grid, and fold them
    // to the ordinal of the page that backs the tile
    auto _ordinal(const index_type & tile) const -> size_type;
    // resolve a python key into box coordinates: one integer per axis, with negative
    // coordinates counting back from the end of their axis
    auto _index(const py::object & key) const -> index_type;

    // implementation details: data
private:
    // the layout; held directly, since only the cell type is erased
    packing_type _packing;
    // the name of the cell type
    string_t _cell;
    // the closures that reach the storage, each built where the cell type was still concrete
    census_type _residents;
    pane_maker_type _pane;
    probe_type _resident;
    probe_type _valid;
    probe_type _clean;
    mark_type _validate;
    mark_type _taint;
    mark_type _flush;
    mark_type _release;
    reader_type _read;
    writer_type _write;
};


// type-erase a mosaic: package the closures that let python reach a concrete
// {Grid<DynamicChunked, Paged<T>>} without knowing {T}
namespace pyre::py::grid {
    // the builder: erase {mosaic} into the single class the bindings expose; {cell} names the
    // cell type in pyre memory vocabulary
    template <class gridT>
    auto anyMosaic(const gridT & mosaic, string_t cell) -> AnyMosaic;
} // namespace pyre::py::grid


// the inline implementations
#include "AnyMosaic.icc"


// end of file
