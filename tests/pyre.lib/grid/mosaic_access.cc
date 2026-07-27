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


// assemble a mosaic, bring every page in, write to every cell, and read them all back
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("mosaic_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.mosaic");

    // pick a box that is not a whole number of tiles
    constexpr shape_t shape { 5, 7 };
    // and a tile extent
    constexpr shape_t tile { 2, 3 };
    // dice the box
    const chunked_t packing { shape, tile };
    // make a store with one page per tile, each page holding one tile's worth of cells
    const paged_t store { packing.tileShape().cells(), packing.tiles().cells() };
    // the two must agree on the total storage
    assert((store.cells() == packing.cells()));
    // put them together: a mosaic
    const mosaic_t mosaic { packing, store };

    // bring every page in, the way a reader that populates the whole product would
    for (auto t : pyre::grid::tilesOverlapping(packing, packing.origin(), packing.shape())) {
        // by asking for the page that backs each tile
        store.reside(packing.tileOrdinal(t));
    }
    // everything is in
    assert((store.residents() == packing.tiles().cells()));

    // fill every cell with a value that encodes where it lives
    for (auto idx : mosaic.packing()) {
        // stamp the cell with its own offset
        mosaic[idx] = static_cast<mosaic_t::value_type>(packing.offset(idx));
    }

    // now go back over the box
    for (auto idx : mosaic.packing()) {
        // work out what the cell should hold
        auto expected = static_cast<mosaic_t::value_type>(packing.offset(idx));
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << mosaic[idx]
                << pyre::journal::newline;
        // the unguarded path must find what we put there
        assert((mosaic[idx] == expected));
        // and so must the guarded one
        assert((mosaic.at(idx) == expected));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
