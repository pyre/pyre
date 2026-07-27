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
// and the pieces used to address it
using shape_t = chunked_t::shape_type;
using index_t = chunked_t::index_type;


// verify that the offset map is the composition of the two nested canonical packings
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("chunked_offset");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.chunked");

    // pick a box that is a whole number of tiles, so every offset is accounted for
    constexpr shape_t shape { 4, 6 };
    // and a tile extent
    constexpr shape_t tile { 2, 3 };
    // dice the box
    constexpr chunked_t packing { shape, tile };

    // the origin sits at the head of the block
    static_assert(packing.offset({ 0, 0 }) == 0);
    // its tile is stored contiguously: stepping along the fast axis within the tile moves one
    // cell at a time
    static_assert(packing.offset({ 0, 1 }) == 1);
    static_assert(packing.offset({ 0, 2 }) == 2);
    // and the next row of the same tile follows immediately
    static_assert(packing.offset({ 1, 0 }) == 3);
    // crossing into the next tile along the second axis skips a full tile of storage
    static_assert(packing.offset({ 0, 3 }) == 6);
    // crossing along the first axis skips a full row of tiles
    static_assert(packing.offset({ 2, 0 }) == 12);
    // the far corner is the last cell of the last tile
    static_assert(packing.offset({ 3, 5 }) == packing.cells() - 1);

    // now verify the whole map against the arithmetic done by hand
    for (auto idx : packing) {
        // the tile the index falls in
        auto tileRow = idx[0] / tile[0];
        auto tileCol = idx[1] / tile[1];
        // and the cell it names within it
        auto cellRow = idx[0] % tile[0];
        auto cellCol = idx[1] % tile[1];
        // the tiles pack in c order, two per row of tiles, six cells each; the cells within a
        // tile pack in c order as well, three per row
        auto expected = (tileRow * 2 + tileCol) * 6 + (cellRow * 3 + cellCol);
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << packing.offset(idx)
                << pyre::journal::newline;
        // the packing must agree
        assert((packing.offset(idx) == expected));
        // and the sugar must match the spelled out form
        assert((packing[idx] == packing.offset(idx)));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // repeat with the box anchored away from zero, on the negative side
    constexpr index_t origin { -2, -3 };
    // same dicing, shifted
    constexpr chunked_t shifted { shape, tile, origin };
    // the origin still lands at the head of the block
    static_assert(shifted.offset(origin) == 0);
    // and the map is translation invariant: shifting the box moves no cell in storage
    for (auto idx : packing) {
        // the shifted packing must place the shifted index where the anchored one placed its own
        assert((shifted.offset(idx + origin) == packing.offset(idx)));
    }

    // all done
    return 0;
}


// end of file
