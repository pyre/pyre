// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>
// and the storage strategies
#include <pyre/memory.h>


// a mosaic: a chunked packing over paged storage
using chunked_t = pyre::grid::chunked_t<2>;
using paged_t = pyre::memory::paged_t<pyre::memory::float64_t>;
using mosaic_t = pyre::grid::mosaic_t<2, pyre::memory::float64_t>;
// and the pieces used to address it
using shape_t = chunked_t::shape_type;
using index_t = chunked_t::index_type;


// the out-of-core workflow: describe a large product for free, find the tiles an algorithm's
// window touches, and materialize a mosaic over just that working set
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("mosaic_window");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.mosaic");

    // the full product: a layout is pure arithmetic, so describing all of it costs nothing;
    // no storage of this size is ever allocated
    constexpr chunked_t full { shape_t { 100, 100 }, shape_t { 10, 10 } };
    // it dices into a hundred tiles
    static_assert(full.tiles().cells() == 100);

    // an algorithm's working window, deliberately not aligned with the tiles
    constexpr index_t base { 35, 42 };
    constexpr shape_t extent { 20, 20 };
    // find the tiles the window touches
    constexpr auto touched = pyre::grid::tilesOverlapping(full, base, extent);
    // the window leans into the tiles at {3,4}
    static_assert(touched.origin() == index_t { 3, 4 });
    // and spills over into a 3x3 block of them
    static_assert(touched.shape() == shape_t { 3, 3 });
    // nine tiles, not a hundred: the working set
    static_assert(touched.cells() == 9);

    // the window mosaic covers the touched tiles, so its box starts at the corner of the first
    // one and spans a whole number of tiles
    const chunked_t packing { touched.shape() * 10l, full.tileShape(),
                              full.tile(touched.origin()).origin() };
    // the aligned box starts where tile {3,4} of the full product does
    assert((packing.origin() == index_t { 30, 40 }));
    // make a store with one page per touched tile
    const paged_t store { packing.tileShape().cells(), packing.tiles().cells() };
    // and assemble the window
    const mosaic_t window { packing, store };

    // bring in the working set, the way a reader pulling chunks from a file would
    for (auto t : pyre::grid::tilesOverlapping(packing, packing.origin(), packing.shape())) {
        // page by page
        auto data = store.reside(packing.tileOrdinal(t));
        // fill each one with something recognizable
        for (paged_t::cell_count_type cell = 0; cell < store.pageCells(); ++cell) {
            // the ordinal of its tile
            data[cell] = static_cast<paged_t::value_type>(packing.tileOrdinal(t));
        }
        // and record that the page now holds meaningful content
        store.validate(packing.tileOrdinal(t));
    }
    // the resident footprint is the working set, nothing more
    assert((store.residents() == 9));
    // which is what bounds the memory bill
    assert((store.bytes() == 9 * 100 * sizeof(paged_t::value_type)));

    // the algorithm addresses the window in the full product's index space
    constexpr index_t probe { 44, 53 };
    // this cell sits in tile {4,5} of the full product
    static_assert(full.tileOf(probe) == index_t { 4, 5 });
    // which the window knows as tile {1,1}, since its own tile grid starts at its corner
    assert((packing.tileOf(probe) == index_t { 1, 1 }));
    // and the cell holds the stamp of its own page
    assert(
        (window[probe]
         == static_cast<mosaic_t::value_type>(packing.tileOrdinal(packing.tileOf(probe)))));
    // show me
    channel << "window: " << store.uri() << pyre::journal::endl(__HERE__);

    // reclaiming the working set is just letting the window go out of scope: pages are never
    // evicted one at a time; the next window is a fresh mosaic
    return 0;
}


// end of file
