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


// verify that a client can manage the memory footprint of a live mosaic through its own
// storage accessor, and that the mosaic keeps functioning while the working set shrinks
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("mosaic_release");

    // pick a box
    constexpr shape_t shape { 4, 6 };
    // and a tile extent
    constexpr shape_t tile { 2, 3 };
    // dice the box
    const chunked_t packing { shape, tile };
    // make a store with one page per tile
    const paged_t store { packing.tileShape().cells(), packing.tiles().cells() };
    // and assemble the mosaic
    const mosaic_t mosaic { packing, store };

    // fill two tiles through their panes
    for (const auto & t : { index_t { 0, 0 }, index_t { 1, 1 } }) {
        // page management is a const operation under the handle model, so the mosaic's own
        // storage accessor is all a client needs to grow the working set
        mosaic.storage().reside(packing.tileOrdinal(t));
        // get the pane
        auto pane = mosaic.pane(t);
        // and stamp every cell with the ordinal of its tile
        for (const auto & idx : pane.packing()) {
            // through the pane, which addresses the mosaic's own cells
            pane[idx] = static_cast<mosaic_t::value_type>(packing.tileOrdinal(t));
        }
        // declare the deposit
        mosaic.storage().validate(packing.tileOrdinal(t));
    }
    // the working set is two pages
    assert((mosaic.storage().residents() == 2));

    // shrink it: let go of the first tile, again through the mosaic's own accessor
    mosaic.storage().release(packing.tileOrdinal(index_t { 0, 0 }));
    // the store forgot the page
    assert((mosaic.storage().residents() == 1));

    // the mosaic keeps functioning: the surviving tile reads back intact
    constexpr index_t probe { 3, 4 };
    // this cell sits in tile {1,1}
    static_assert(chunked_t(shape, tile).tileOf(probe) == index_t { 1, 1 });
    // and still holds its stamp
    assert(
        (mosaic[probe]
         == static_cast<mosaic_t::value_type>(packing.tileOrdinal(packing.tileOf(probe)))));

    // the released tile is indistinguishable from one never touched: bringing it back in
    // materializes a fresh page
    mosaic.storage().reside(packing.tileOrdinal(index_t { 0, 0 }));
    // whose pane is writable all over again
    auto pane = mosaic.pane(index_t { 0, 0 });
    // deposit a fresh value
    pane[index_t { 0, 0 }] = 42;
    // and the mosaic sees it
    assert((mosaic[index_t { 0, 0 }] == 42));

    // all done
    return 0;
}


// end of file
