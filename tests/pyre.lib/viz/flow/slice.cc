// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the factory that copies a window of a raster into a tile: it samples every {stride} cell
// starting at {origin}, counted in strides, from a raster that owns its cells or one that wraps
// cells it borrows; moving the window makes the tile stale; a window that does not fit is
// reported; and its settings work by name


// portability
#include <portinfo>
// STL
#include <cassert>
#include <vector>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
// all tiles are two dimensional
using packing_t = pyre::grid::canonical_t<2>;
using shape_t = packing_t::shape_type;
// a tile of floats on the heap
using tile_t =
    pyre::flow::products::tile_t<pyre::grid::grid_t<packing_t, pyre::memory::heap_t<float>>>;
// a grid over floats that live elsewhere, and a tile over it
using view_t = pyre::grid::grid_t<packing_t, pyre::memory::constview_t<float>>;
using raster_t = pyre::flow::products::tile_t<view_t>;
// the factories
using slice_t = pyre::flow::factories::sources::slice_t<raster_t, tile_t>;
using heapslice_t = pyre::flow::factories::sources::slice_t<tile_t, tile_t>;
using normalizer_t = pyre::flow::factories::filters::parametric_t<tile_t, tile_t>;
// settings
using pair_t = pyre::flow::pair_t;
using interval_t = pyre::flow::interval_t;
// the catalog
using catalog_t = pyre::flow::catalog::catalog_t;


// driver
int
main(int argc, char * argv[])
{
    // the shape of the raster
    const int lines = 6;
    const int samples = 8;
    // its cells, which live in a vector, as the cells of a memory mapped file live elsewhere
    auto cells = std::vector<float>(lines * samples);
    // each one holds 10 times its line plus its sample
    for (int line = 0; line < lines; ++line) {
        // one sample at a time
        for (int sample = 0; sample < samples; ++sample) {
            // so a cell says where it is
            cells[line * samples + sample] = 10.0f * line + sample;
        }
    }
    // a grid over them
    auto grid = view_t(
        packing_t(shape_t { lines, samples }),
        pyre::memory::constview_t<float>(cells.data(), cells.size()));
    // and a tile over the grid, which shares its cells
    auto raster = raster_t::create("raster", grid);
    // which starts fresh, since its cells hold what they hold
    assert(!raster->stale());

    // a tile of two lines and three samples
    auto tile = tile_t::create("tile", shape_t { 2, 3 }, 0.0f);
    // a slice that starts at the second line and sample, counted in strides, every other cell
    auto slice = slice_t::create("slice", pair_t { 1, 1 }, pair_t { 2, 2 });
    // wire it
    slice->source(raster);
    slice->slice(tile);

    // pull the tile
    const auto & first = tile->read();
    // the cell at {row, column} is the one of the raster at {(1 + row) * 2, (1 + column) * 2}
    for (int row = 0; row < 2; ++row) {
        // one column at a time
        for (int column = 0; column < 3; ++column) {
            // check
            assert(first[row * 3 + column] == 10.0f * (2 + 2 * row) + (2 + 2 * column));
        }
    }

    // moving the window
    slice->origin(pair_t { 0, 0 });
    // makes the tile stale
    assert(tile->stale());
    // and the next pull reads the new window
    assert(tile->read()[0] == 0.0f && tile->read()[5] == 10.0f * 2 + 4);

    // the settings, by name, the way an inspector changes them
    std::shared_ptr<pyre::flow::factory_t> factory = slice;
    // are the origin and the stride, both pairs
    assert(factory->settings().size() == 2);
    assert(factory->settings()[0].name() == "origin" && factory->settings()[0].type() == "pair");
    assert(factory->settings()[1].name() == "stride" && factory->settings()[1].type() == "pair");
    // a new stride
    assert(factory->set("stride", pair_t { 1, 1 }));
    // makes the tile stale
    assert(tile->stale());
    // and reads adjacent cells
    assert(tile->read()[1] == 1.0f);
    // an interval is no pair
    assert(!factory->set("stride", interval_t { 1, 1 }));
    // and the stride is as it was
    assert(slice->stride() == pair_t(1, 1));

    // a window that does not fit
    slice->origin(pair_t { 5, 0 });
    // is reported, quietly here
    pyre::journal::error_t::quiet();
    // by raising
    try {
        // pull the tile
        tile->read();
        // so we can't get here
        assert(false);
    } catch (const pyre::journal::application_error &) {
        // as expected
    }

    // a slice of a raster that owns its cells works the same way
    auto owned = tile_t::create("owned", shape_t { lines, samples }, 1.0f);
    auto copy = tile_t::create("copy", shape_t { 2, 2 }, 0.0f);
    auto other = heapslice_t::create("other");
    other->source(owned);
    other->slice(copy);
    assert(copy->read()[3] == 1.0f);

    // the catalog files a tile that wraps cells it does not own
    auto catalog = catalog_t();
    catalog.registerProduct<raster_t>();
    // with the spelling of its cells
    assert(catalog.product(raster_t::declSelf())->cell() == "float");
    // but cannot make one from a shape, since its cells come from elsewhere
    assert(!catalog.product(raster_t::declSelf())->makes());
    assert(catalog.makeProduct(raster_t::declSelf(), "nothing", shape_t { 2, 2 }) == nullptr);
    // while it describes the slice
    catalog.registerFactory<slice_t>();
    assert(catalog.factory(slice_t::declSelf())->slots()[0].product() == raster_t::declSelf());

    // a pair of integers widens into an interval, which is how python hands one over
    auto normalizer = normalizer_t::create("normalizer");
    std::shared_ptr<pyre::flow::factory_t> filter = normalizer;
    assert(filter->set("interval", pair_t { 0, 10 }));
    assert(normalizer->interval() == interval_t(0, 10));

    // all done
    return 0;
}


// end of file
