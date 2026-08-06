// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <algorithm>
#include <cassert>
#include <vector>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test
using chunked_t = pyre::grid::chunked_t<2>;
// and the pieces used to address it
using shape_t = chunked_t::shape_type;


// verify that distinct indices land on distinct offsets, and that the padding is never touched
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("chunked_injective");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.chunked");

    // pick a box that is not a whole number of tiles, so the edge tiles overhang
    constexpr shape_t shape { 5, 5 };
    // the tile extent
    constexpr shape_t tile { 2, 2 };
    // dice the box
    constexpr chunked_t packing { shape, tile };

    // a tally with one slot per cell of storage, all unclaimed
    std::vector<char> claimed(packing.cells(), 0);
    // sweep the box
    for (auto idx : packing) {
        // find where this index lands
        auto offset = packing.offset(idx);
        // it must fall within the storage the packing asked for
        assert((offset >= 0 && offset < packing.cells()));
        // no earlier index may have claimed it
        assert((claimed[offset] == 0));
        // it is now spoken for
        claimed[offset] = 1;
    }

    // count the claimed cells
    auto used = std::count(claimed.begin(), claimed.end(), 1);
    // every index in the box claimed exactly one cell
    assert((used == shape.cells()));
    // and the rest of the storage is the padding of the overhanging edge tiles: nine tiles of
    // four cells each, minus the twenty five cells the box addresses
    assert((packing.cells() - used == 9 * 4 - 25));
    // show me
    channel << pyre::journal::at() << "cells: " << packing.cells() << pyre::journal::newline
            << "used: " << used << pyre::journal::newline << "padding: " << packing.cells() - used
            << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
