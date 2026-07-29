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
#include "__init__.h"
// the type-erased grid and its converters
#include "AnyGrid.h"
// and the type-erased mosaic, its out-of-core sibling
#include "AnyMosaic.h"


// the type-erased grid measures with a signed integer, matching the c++ library
using size_type = pyre::py::grid::AnyGrid::size_type;


// the factories all build over a runtime-rank packing, so that they dispatch on the cell type
// alone: twelve leaf instantiations per storage strategy, never a span of ranks as well
namespace pyre::py::grid {
    // the runtime-rank packing
    using packing_t = pyre::grid::dynamic_canonical_t;
    // its shape carries one signed extent per axis
    using shape_t = packing_t::shape_type;

    // choose a cell type from its pyre memory cell name and hand it to a callable that is
    // templated on that type; this keeps the twelve-way dispatch in one place, and the return
    // type is deduced so both grid and mosaic factories can ride it
    template <class F>
    auto dispatchCell(const string_t & cell, F && f)
    {
        // signed integers
        if (cell == "int8")
            return f.template operator()<pyre::memory::int8_t>();
        if (cell == "int16")
            return f.template operator()<pyre::memory::int16_t>();
        if (cell == "int32")
            return f.template operator()<pyre::memory::int32_t>();
        if (cell == "int64")
            return f.template operator()<pyre::memory::int64_t>();
        // unsigned integers
        if (cell == "uint8")
            return f.template operator()<pyre::memory::uint8_t>();
        if (cell == "uint16")
            return f.template operator()<pyre::memory::uint16_t>();
        if (cell == "uint32")
            return f.template operator()<pyre::memory::uint32_t>();
        if (cell == "uint64")
            return f.template operator()<pyre::memory::uint64_t>();
        // floating point
        if (cell == "float32")
            return f.template operator()<pyre::memory::float32_t>();
        if (cell == "float64")
            return f.template operator()<pyre::memory::float64_t>();
        // complex
        if (cell == "complex64")
            return f.template operator()<pyre::memory::complex64_t>();
        if (cell == "complex128")
            return f.template operator()<pyre::memory::complex128_t>();

        // anything else is a caller mistake
        auto channel = pyre::journal::error_t("pyre.grid.bindings");
        // complain
        channel << "unsupported grid cell type '" << cell << "'" << pyre::journal::endl(__HERE__);
        // and refuse
        throw py::value_error("unsupported grid cell type '" + cell + "'");
    }


    // a heap grid: allocate a fresh block of {shape} cells of type {cellT}
    template <class cellT>
    auto makeHeap(const shape_t & shape) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::heap_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // put enough cells on the heap
        auto storage = storage_t { packing.cells() };
        // make the grid and type-erase it; heap storage owns its cells
        return anyGrid(grid_t { packing, storage }, "heap");
    }

    // the heap factory python calls
    auto heap(const std::vector<size_type> & extents, const string_t & cell) -> AnyGrid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeHeap<T>(shape); });
    }


    // a file-backed grid: lay {shape} cells of {cellT} over the product at {uri}
    // {create} chooses between making a fresh product sized to the shape, and mapping an
    // existing one, which is how a data product on disk is read back
    template <class cellT>
    auto makeMap(const string_t & uri, const shape_t & shape, bool create) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::map_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // either make a file large enough to hold the grid, or map an existing one for writing
        auto storage =
            create ? storage_t::create(uri, packing.cells()) : storage_t::open(uri, true);
        // make the grid and type-erase it; map storage owns its cells through a shared handle
        return anyGrid(grid_t { packing, storage }, "map");
    }

    // the map factory python calls
    auto map(
        const string_t & uri, const std::vector<size_type> & extents, const string_t & cell,
        bool create) -> AnyGrid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeMap<T>(uri, shape, create); });
    }


    // a non-owning grid over memory python already holds: lay a {shape} of {cellT} cells over the
    // block the {source} buffer exports, without copying
    template <class cellT>
    auto makeView(const py::buffer & source, const shape_t & shape) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::view_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // the number of cells the grid needs
        auto cells = packing.cells();

        // ask the source for writable access to its block
        auto info = std::make_shared<py::buffer_info>(source.request(true));
        // the block must be at least as large as the grid
        if (info->size < cells) {
            // otherwise the caller has made a mistake
            throw py::value_error("source buffer is too small for the requested grid shape");
        }
        // and its cells must be the width we were told to expect
        if (info->itemsize != static_cast<py::ssize_t>(sizeof(cellT))) {
            // otherwise the cell and the buffer disagree
            throw py::value_error("source buffer cell size does not match the requested cell");
        }

        // a view over the source's memory
        auto storage = storage_t(static_cast<cellT *>(info->ptr), cells);
        // paired with the layout
        auto grid = grid_t { packing, storage };
        // the view owns nothing, so keep the source's buffer view open for as long as python
        // holds the type-erased grid; that pins both the exporter and its block
        return describe(grid, "view", info->ptr, info);
    }

    // the view factory python calls
    auto view(
        const py::buffer & source, const std::vector<size_type> & extents, const string_t & cell)
        -> AnyGrid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeView<T>(source, shape); });
    }


    // a mosaic: an out-of-core grid of {shape} cells of {cellT}, diced into tiles of extent
    // {tile}, over a store with one demand-materialized page per tile
    template <class cellT>
    auto makeMosaic(const shape_t & shape, const shape_t & tile, const string_t & cell) -> AnyMosaic
    {
        // the tiled layout, the storage, and the grid over them
        using chunked_t = pyre::grid::dynamic_chunked_t;
        using storage_t = pyre::memory::paged_t<cellT>;
        using grid_t = pyre::grid::grid_t<chunked_t, storage_t>;
        // dice the box
        auto packing = chunked_t(shape, tile);
        // a page holds a full tile's worth of cells
        typename storage_t::cell_count_type pageCells = 1;
        // measured axis by axis
        for (auto extent : packing.tileShape()) {
            // as the volume of one tile
            pageCells *= extent;
        }
        // and there is one page per tile
        typename storage_t::cell_count_type pages = 1;
        // likewise
        for (auto extent : packing.tiles()) {
            // the volume of the tile grid
            pages *= extent;
        }
        // make a store with nothing resident: describing the product is free, and pages get
        // allocated only as python touches their tiles
        auto storage = storage_t { pageCells, pages };
        // assemble the mosaic and type-erase it
        return anyMosaic(grid_t { packing, storage }, cell);
    }

    // the mosaic factory python calls
    auto mosaic(
        const std::vector<size_type> & extents, const std::vector<size_type> & tile,
        const string_t & cell) -> AnyMosaic
    {
        // adopt the extents as shapes
        auto shape = shape_t(extents.begin(), extents.end());
        auto tileShape = shape_t(tile.begin(), tile.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeMosaic<T>(shape, tileShape, cell); });
    }
} // namespace pyre::py::grid


// build the {grid} submodule
auto
pyre::py::grid::__init__(py::module & m) -> void
{
    // make the submodule
    auto grid = m.def_submodule(
        // the name
        "grid",
        // the docstring
        "multi-dimensional arrays over pluggable memory");

    // the single type-erased grid class, presenting the python buffer protocol so any consumer of
    // that protocol can view its cells with no copy
    auto cls = py::class_<AnyGrid>(
        // in the submodule
        grid,
        // named
        "Grid",
        // exposing the buffer protocol
        py::buffer_protocol(),
        // the docstring
        "a multi-dimensional array whose cells live behind a storage strategy");

    // wire the buffer protocol to the type-erased grid's own description
    cls.def_buffer([](AnyGrid & self) -> py::buffer_info { return self.view(); });

    // the extent along each axis
    cls.def_property_readonly(
        // the name
        "shape",
        // the getter
        &AnyGrid::shape,
        // the docstring
        "my extent along each axis");

    // the strides, in cells
    cls.def_property_readonly(
        // the name
        "strides",
        // the getter
        &AnyGrid::strides,
        // the docstring
        "the distance between consecutive cells along each axis, in cells");

    // the number of axes
    cls.def_property_readonly(
        // the name
        "rank",
        // the getter
        &AnyGrid::rank,
        // the docstring
        "my number of axes");

    // whether my cells may be written
    cls.def_property_readonly(
        // the name
        "writable",
        // the getter
        &AnyGrid::writable,
        // the docstring
        "whether python may write through to my cells");

    // the storage strategy that backs me
    cls.def_property_readonly(
        // the name
        "strategy",
        // the getter
        &AnyGrid::strategy,
        // the docstring
        "the storage strategy that holds my cells");

    // read access: {g[i, j, ...]}
    cls.def(
        // the name
        "__getitem__",
        // the implementation
        &AnyGrid::getitem,
        // the signature
        "index"_a,
        // the docstring
        "the cell at a full index, or a sub-grid for a partial or sliced {index}");

    // write access: {g[i, j, ...] = v}
    cls.def(
        // the name
        "__setitem__",
        // the implementation
        &AnyGrid::setitem,
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "write {value} into the cell at a full integer {index}");

    // the type-erased mosaic: an out-of-core grid whose cells live on demand-materialized
    // pages, one per tile, reached tile by tile through zero-copy panes
    auto mos = py::class_<AnyMosaic>(
        // in the submodule
        grid,
        // named
        "Mosaic",
        // the docstring
        "an out-of-core grid whose tiles materialize on demand and travel as zero-copy panes");

    // the extent along each axis
    mos.def_property_readonly(
        // the name
        "shape",
        // the getter
        &AnyMosaic::shape,
        // the docstring
        "my extent along each axis");

    // the smallest addressable index
    mos.def_property_readonly(
        // the name
        "origin",
        // the getter
        &AnyMosaic::origin,
        // the docstring
        "my smallest addressable index");

    // the number of axes
    mos.def_property_readonly(
        // the name
        "rank",
        // the getter
        &AnyMosaic::rank,
        // the docstring
        "my number of axes");

    // the extent of the grid of tiles
    mos.def_property_readonly(
        // the name
        "tiles",
        // the getter
        &AnyMosaic::tiles,
        // the docstring
        "the extent of my grid of tiles");

    // the extent of one tile
    mos.def_property_readonly(
        // the name
        "tileShape",
        // the getter
        &AnyMosaic::tileShape,
        // the docstring
        "the extent of one of my tiles");

    // the storage bill
    mos.def_property_readonly(
        // the name
        "cells",
        // the getter
        &AnyMosaic::cells,
        // the docstring
        "the number of cells my storage supplies: every tile at full size, padding included");

    // the name of the cell type
    mos.def_property_readonly(
        // the name
        "cell",
        // the getter
        &AnyMosaic::cell,
        // the docstring
        "the name of my cell type");

    // the resident census
    mos.def_property_readonly(
        // the name
        "residents",
        // the getter
        &AnyMosaic::residents,
        // the docstring
        "the number of my pages that are actually resident");

    // the tile a given index falls in
    mos.def(
        // the name
        "tileOf",
        // the implementation
        &AnyMosaic::tileOf,
        // the signature
        "index"_a,
        // the docstring
        "the coordinates, in my grid of tiles, of the tile {index} falls in");

    // the working set of a window
    mos.def(
        // the name
        "tilesOverlapping",
        // the implementation
        &AnyMosaic::tilesOverlapping,
        // the signature
        "base"_a, "shape"_a,
        // the docstring
        "the tiles touched by the box anchored at {base} with the given {shape}");

    // the pane over a tile
    mos.def(
        // the name
        "pane",
        // the implementation
        &AnyMosaic::pane,
        // the signature
        "tile"_a,
        // the docstring
        "a dense zero-copy grid over the page that holds {tile}, materializing it on first "
        "touch");

    // read access: {m[i, j, ...]}
    mos.def(
        // the name
        "__getitem__",
        // the implementation
        &AnyMosaic::getitem,
        // the signature
        "index"_a,
        // the docstring
        "the cell at a full integer {index}; its page must be resident");

    // write access: {m[i, j, ...] = v}
    mos.def(
        // the name
        "__setitem__",
        // the implementation
        &AnyMosaic::setitem,
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "write {value} into the cell at a full integer {index}, materializing its page on "
        "first touch and tainting it");

    // the page state probes
    mos.def(
        // the name
        "resident",
        // the implementation
        &AnyMosaic::resident,
        // the signature
        "tile"_a,
        // the docstring
        "whether the page that backs {tile} has been allocated");

    mos.def(
        // the name
        "valid",
        // the implementation
        &AnyMosaic::valid,
        // the signature
        "tile"_a,
        // the docstring
        "whether meaningful content has been deposited in {tile}");

    mos.def(
        // the name
        "clean",
        // the implementation
        &AnyMosaic::clean,
        // the signature
        "tile"_a,
        // the docstring
        "whether the content of {tile} matches my backing store");

    // and the page state marks
    mos.def(
        // the name
        "validate",
        // the implementation
        &AnyMosaic::validate,
        // the signature
        "tile"_a,
        // the docstring
        "record that meaningful content has been deposited in {tile}");

    mos.def(
        // the name
        "taint",
        // the implementation
        &AnyMosaic::taint,
        // the signature
        "tile"_a,
        // the docstring
        "record that {tile} has been written to, so it diverges from my backing store");

    mos.def(
        // the name
        "flush",
        // the implementation
        &AnyMosaic::flush,
        // the signature
        "tile"_a,
        // the docstring
        "record that {tile} has been saved, so it matches my backing store again");

    // the factory that allocates a fresh heap grid
    grid.def(
        // the name
        "heap",
        // the implementation
        &heap,
        // the signature
        "shape"_a, "cell"_a,
        // the docstring
        "make a grid over a fresh block of heap memory of the given {shape} and {cell}");

    // the factory that maps a file-backed grid
    grid.def(
        // the name
        "map",
        // the implementation
        &map,
        // the signature; {create} makes a fresh product, else an existing one is mapped for
        // writing, which is how a data product on disk is read back
        "uri"_a, "shape"_a, "cell"_a, "create"_a = true,
        // the docstring
        "lay a grid of the given {shape} and {cell} over the memory-mapped file at {uri}");

    // the factory that wraps memory python already holds
    grid.def(
        // the name
        "view",
        // the implementation
        &view,
        // the signature
        "source"_a, "shape"_a, "cell"_a,
        // the docstring
        "lay a grid of the given {shape} and {cell} over the memory of the {source} buffer, "
        "without copying");

    // the factory that describes an out-of-core mosaic
    grid.def(
        // the name
        "mosaic",
        // the implementation
        &mosaic,
        // the signature
        "shape"_a, "tile"_a, "cell"_a,
        // the docstring
        "describe an out-of-core grid of the given {shape} and {cell}, diced into tiles of "
        "extent {tile}; nothing is allocated until a tile is touched");

    // all done
    return;
}


// end of file
