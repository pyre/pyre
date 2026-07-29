// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the runtime rank layout under test, and the compile time one that serves as the oracle
using dynamic_t = pyre::grid::dynamic_chunked_t;
using chunked_t = pyre::grid::chunked_t<2>;
// the pieces used to address the static flavor
using shape_t = chunked_t::shape_type;
using index_t = chunked_t::index_type;


// verify that the runtime rank chunked layout realizes the same isomorphism as the compile
// time one
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dynamic_chunked_sanity");

    // pick a box that is not a whole number of tiles, so the edge padding is in play
    constexpr shape_t shape { 7, 5 };
    // a tile extent
    constexpr shape_t tile { 3, 2 };
    // and a placement away from zero, so the origin arithmetic is exercised too
    constexpr index_t origin { -1, 2 };

    // dice the box the compile time way
    constexpr chunked_t oracle { shape, tile, origin };
    // and the runtime way
    const dynamic_t packing { { 7, 5 }, { 3, 2 }, { -1, 2 } };

    // the rank is discovered from the extents
    assert((packing.rank() == 2));
    // the box is what was asked for
    assert((packing.shape() == dynamic_t::shape_type { 7, 5 }));
    // parked where it was asked to sit
    assert((packing.origin() == dynamic_t::index_type { -1, 2 }));
    // the tile extent survives
    assert((packing.tileShape() == dynamic_t::shape_type { 3, 2 }));
    // the box needs as many tiles as the oracle says: enough to cover it, edges rounded up
    assert((packing.tiles() == dynamic_t::shape_type { 3, 3 }));
    // and the storage bill includes the padding of the overhanging tiles
    assert((packing.cells() == oracle.cells()));

    // sweep the entire box
    for (const auto & idx : oracle) {
        // spell the index the runtime way
        const dynamic_t::index_type didx { idx[0], idx[1] };
        // the two layouts must agree on where the cell lives
        assert((packing.offset(didx) == oracle.offset(idx)));
        // on which tile it falls in
        const auto tileOf = oracle.tileOf(idx);
        assert((packing.tileOf(didx) == dynamic_t::index_type { tileOf[0], tileOf[1] }));
        // and on where that tile sits in the packing sequence
        assert(
            (packing.tileOrdinal(packing.tileOf(didx)) == oracle.tileOrdinal(oracle.tileOf(idx))));
    }

    // pick a tile
    const dynamic_t::index_type t { 1, 2 };
    // and derive its self-contained layout
    const auto pane = packing.tile(t);
    // its box is one full tile, overhang included
    assert((pane.shape() == packing.tileShape()));
    // anchored at the tile's own corner of the index space, per the oracle
    const auto anchor = oracle.tile(index_t { 1, 2 }).origin();
    assert((pane.origin() == dynamic_t::index_type { anchor[0], anchor[1] }));
    // and it is dense: it packs exactly a tile's worth of cells
    assert((pane.cells() == oracle.tile(index_t { 1, 2 }).cells()));

    // all done
    return 0;
}


// end of file
