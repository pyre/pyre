// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test
using chunked_t = pyre::grid::chunked_t<2>;


// sanity check: verify that a chunked layout reports its geometry correctly
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("chunked_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.chunked");

    // pick a box whose extent is not a whole number of tiles, so the padding is in play
    constexpr chunked_t::shape_type shape { 5, 4 };
    // and a tile extent
    constexpr chunked_t::shape_type tile { 2, 3 };
    // dice the box
    constexpr chunked_t packing { shape, tile };
    // show me
    channel << "shape: " << packing.shape() << pyre::journal::newline
            << "tile: " << packing.tileShape() << pyre::journal::newline
            << "tiles: " << packing.tiles() << pyre::journal::newline
            << "cells: " << packing.cells() << pyre::journal::endl(__HERE__);

    // the box is what i asked for
    static_assert(packing.shape() == shape);
    // anchored at zero by default
    static_assert(packing.origin() == chunked_t::index_type::zero());
    // the tiles are the extent i specified
    static_assert(packing.tileShape() == tile);
    // covering the box takes three tiles along the first axis and two along the second, with
    // the last ones overhanging the edge
    static_assert(packing.tiles() == chunked_t::shape_type { 3, 2 });
    // the rank is a compile time constant
    static_assert(packing.rank() == 2);

    // the storage requirement is every tile at full size: six tiles of six cells each, well
    // more than the twenty cells the box actually addresses
    static_assert(packing.cells() == 36);

    // all done
    return 0;
}


// end of file
