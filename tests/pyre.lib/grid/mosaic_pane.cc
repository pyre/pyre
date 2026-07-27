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


// verify that a pane is a zero-copy dense grid over one tile of a mosaic
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("mosaic_pane");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.mosaic");

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

    // pick a tile
    constexpr index_t t { 1, 1 };
    // the page that backs it
    auto ordinal = packing.tileOrdinal(t);
    // bring it in; nothing else becomes resident
    store.reside(ordinal);

    // get the pane: a dense grid over just this tile
    auto pane = mosaic.pane(t);
    // its box is one tile
    assert((pane.packing().shape() == packing.tileShape()));
    // anchored where the tile lives in the mosaic's index space
    assert((pane.packing().origin() == index_t { 2, 3 }));
    // and it is contiguous, so it can hand out its address: the page itself, no copy anywhere
    assert((pane.data() == store.page(ordinal)));

    // write through the pane
    for (auto idx : pane.packing()) {
        // stamping each cell with the mosaic offset of its index
        pane[idx] = static_cast<mosaic_t::value_type>(packing.offset(idx));
    }
    // the client deposited content and diverged from any backing store; say so
    store.validate(ordinal);
    store.taint(ordinal);

    // the pane's indices are mosaic indices, so the mosaic must see every write
    for (auto idx : pane.packing()) {
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << mosaic[idx]
                << pyre::journal::newline;
        // read back through the mosaic
        assert((mosaic[idx] == static_cast<mosaic_t::value_type>(packing.offset(idx))));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // and a write through the mosaic is visible through the pane
    mosaic[index_t { 3, 4 }] = 42;
    // no copies anywhere: same cell
    assert((pane[index_t { 3, 4 }] == 42));

    // all done
    return 0;
}


// end of file
