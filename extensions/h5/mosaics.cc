// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// the mosaic machinery
#include "mosaics.h"


// build the module-local flavors of the type-erased classes
// {Grid} and {Mosaic} are also registered by the {pyre} extension; each module keeps its own
// python flavor so that no registered type ever has to cross an extension boundary, where
// type identity is at the mercy of the dynamic loader; values travel between the two worlds
// through the buffer protocol, which is module-blind by construction
auto
pyre::h5::py::mosaics(py::module & m) -> void
{
    // the type-erased grid: the panes of a mosaic travel as these
    auto grid = py::class_<anygrid_t>(
        // in the module
        m,
        // named
        "Grid",
        // exposing the buffer protocol
        py::buffer_protocol(),
        // visible only within this module
        py::module_local(),
        // the docstring
        "a dense grid over one page of a mosaic");

    // wire the buffer protocol to the grid's own description
    grid.def_buffer([](anygrid_t & self) -> py::buffer_info { return self.view(); });

    // the extent along each axis
    grid.def_property_readonly(
        // the name
        "shape",
        // the getter
        &anygrid_t::shape,
        // the docstring
        "my extent along each axis");

    // the strides, in cells
    grid.def_property_readonly(
        // the name
        "strides",
        // the getter
        &anygrid_t::strides,
        // the docstring
        "the distance between consecutive cells along each axis, in cells");

    // the number of axes
    grid.def_property_readonly(
        // the name
        "rank",
        // the getter
        &anygrid_t::rank,
        // the docstring
        "my number of axes");

    // whether python may write through
    grid.def_property_readonly(
        // the name
        "writable",
        // the getter
        &anygrid_t::writable,
        // the docstring
        "whether python may write through to my cells");

    // the storage strategy
    grid.def_property_readonly(
        // the name
        "strategy",
        // the getter
        &anygrid_t::strategy,
        // the docstring
        "the storage strategy that holds my cells");

    // read access
    grid.def(
        // the name
        "__getitem__",
        // the implementation
        &anygrid_t::getitem,
        // the signature
        "index"_a,
        // the docstring
        "the cell at a full index, or a sub-grid for a partial or sliced {index}");

    // write access
    grid.def(
        // the name
        "__setitem__",
        // the implementation
        &anygrid_t::setitem,
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "write {value} into the cell at a full integer {index}");

    // the type-erased mosaic, wired to a dataset by the {mosaic} factories
    auto mos = py::class_<anymosaic_t>(
        // in the module
        m,
        // named
        "Mosaic",
        // visible only within this module
        py::module_local(),
        // the docstring
        "an out-of-core view of a chunked dataset: chunks materialize as they are filled, "
        "and travel as zero-copy panes");

    // the extent along each axis
    mos.def_property_readonly(
        // the name
        "shape",
        // the getter
        &anymosaic_t::shape,
        // the docstring
        "my extent along each axis");

    // the smallest addressable index
    mos.def_property_readonly(
        // the name
        "origin",
        // the getter
        &anymosaic_t::origin,
        // the docstring
        "my smallest addressable index");

    // the number of axes
    mos.def_property_readonly(
        // the name
        "rank",
        // the getter
        &anymosaic_t::rank,
        // the docstring
        "my number of axes");

    // the extent of the grid of tiles
    mos.def_property_readonly(
        // the name
        "tiles",
        // the getter
        &anymosaic_t::tiles,
        // the docstring
        "the extent of my grid of tiles");

    // the extent of one tile
    mos.def_property_readonly(
        // the name
        "tileShape",
        // the getter
        &anymosaic_t::tileShape,
        // the docstring
        "the extent of one of my tiles");

    // the storage bill
    mos.def_property_readonly(
        // the name
        "cells",
        // the getter
        &anymosaic_t::cells,
        // the docstring
        "the number of cells my storage supplies: every tile at full size, padding included");

    // the name of the cell type
    mos.def_property_readonly(
        // the name
        "cell",
        // the getter
        &anymosaic_t::cell,
        // the docstring
        "the name of my cell type");

    // the resident census
    mos.def_property_readonly(
        // the name
        "residents",
        // the getter
        &anymosaic_t::residents,
        // the docstring
        "the number of my pages that are actually resident");

    // whether i have a backing store
    mos.def_property_readonly(
        // the name
        "connected",
        // the getter
        &anymosaic_t::connected,
        // the docstring
        "whether i am wired to a backing store");

    // the tile a given index falls in
    mos.def(
        // the name
        "tileOf",
        // the implementation
        &anymosaic_t::tileOf,
        // the signature
        "index"_a,
        // the docstring
        "the coordinates, in my grid of tiles, of the tile {index} falls in");

    // the working set of a window
    mos.def(
        // the name
        "tilesOverlapping",
        // the implementation
        &anymosaic_t::tilesOverlapping,
        // the signature
        "base"_a, "shape"_a,
        // the docstring
        "the tiles touched by the box anchored at {base} with the given {shape}");

    // the pane over a tile
    mos.def(
        // the name
        "pane",
        // the implementation
        &anymosaic_t::pane,
        // the signature
        "tile"_a,
        // the docstring
        "a dense zero-copy grid over the page that holds {tile}, materializing it on first "
        "touch");

    // read access
    mos.def(
        // the name
        "__getitem__",
        // the implementation
        &anymosaic_t::getitem,
        // the signature
        "index"_a,
        // the docstring
        "the cell at a full integer {index}; its page must be resident");

    // write access
    mos.def(
        // the name
        "__setitem__",
        // the implementation
        &anymosaic_t::setitem,
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "write {value} into the cell at a full integer {index}, materializing its page on "
        "first touch and tainting it");

    // pull one chunk from the backing store
    mos.def(
        // the name
        "fill",
        // the implementation; the per-tile flavor
        py::overload_cast<const anymosaic_t::index_type &>(&anymosaic_t::fill, py::const_),
        // the signature
        "tile"_a,
        // the docstring
        "pull the chunk at {tile} from my backing store into its page");

    // pull everything
    mos.def(
        // the name
        "fill",
        // the implementation; the wholesale flavor
        py::overload_cast<>(&anymosaic_t::fill, py::const_),
        // the docstring
        "pull every chunk of my box from my backing store");

    // push one chunk to the backing store
    mos.def(
        // the name
        "flush",
        // the implementation; the per-tile flavor
        py::overload_cast<const anymosaic_t::index_type &>(&anymosaic_t::flush, py::const_),
        // the signature
        "tile"_a,
        // the docstring
        "make my backing store agree about {tile}: push its page and mark it");

    // push what diverged
    mos.def(
        // the name
        "flush",
        // the implementation; the wholesale flavor
        py::overload_cast<>(&anymosaic_t::flush, py::const_),
        // the docstring
        "make my backing store agree with me: push every page that is resident and has "
        "diverged");

    // the page state probes
    mos.def(
        // the name
        "resident",
        // the implementation
        &anymosaic_t::resident,
        // the signature
        "tile"_a,
        // the docstring
        "whether the page that backs {tile} has been allocated");

    mos.def(
        // the name
        "valid",
        // the implementation
        &anymosaic_t::valid,
        // the signature
        "tile"_a,
        // the docstring
        "whether meaningful content has been deposited in {tile}");

    mos.def(
        // the name
        "clean",
        // the implementation
        &anymosaic_t::clean,
        // the signature
        "tile"_a,
        // the docstring
        "whether the content of {tile} matches my backing store");

    // and the page state marks
    mos.def(
        // the name
        "validate",
        // the implementation
        &anymosaic_t::validate,
        // the signature
        "tile"_a,
        // the docstring
        "record that meaningful content has been deposited in {tile}");

    mos.def(
        // the name
        "taint",
        // the implementation
        &anymosaic_t::taint,
        // the signature
        "tile"_a,
        // the docstring
        "record that {tile} has been written to, so it diverges from my backing store");

    mos.def(
        // the name
        "release",
        // the implementation
        &anymosaic_t::release,
        // the signature
        "tile"_a,
        // the docstring
        "let go of the page that backs {tile}, returning it to the never-touched state; "
        "outstanding panes keep their memory but no longer alias my cells");

    // all done
    return;
}


// end of file
