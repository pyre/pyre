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


// exercise the tiling interface: locating the tile an index falls in, and numbering the tiles
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("chunked_tiles");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.chunked");

    // pick a box that is not a whole number of tiles, anchored away from zero
    constexpr shape_t shape { 5, 7 };
    // the tile extent
    constexpr shape_t tile { 2, 3 };
    // and the anchor
    constexpr index_t origin { 10, -20 };
    // dice the box
    constexpr chunked_t packing { shape, tile, origin };

    // the origin falls in the first tile
    static_assert(packing.tileOf(origin) == index_t::zero());
    // which is the first one in the packing sequence
    static_assert(packing.tileOrdinal(index_t::zero()) == 0);
    // the far corner falls in the last tile
    static_assert(packing.tileOf({ 14, -14 }) == index_t { 2, 2 });
    // which is the last one in the sequence
    static_assert(packing.tileOrdinal(index_t { 2, 2 }) == 8);

    // the storage footprint of one tile
    const auto tileCells = packing.tileShape().cells();
    // sweep the box
    for (auto idx : packing) {
        // locate the tile this index falls in
        auto t = packing.tileOf(idx);
        // its coordinates must fall within the grid of tiles
        for (std::size_t axis = 0; axis < packing.rank(); ++axis) {
            // on the low side
            assert((t[axis] >= 0));
            // and the high one
            assert((t[axis] < packing.tiles()[axis]));
        }
        // the tile's rank in the packing sequence
        auto ordinal = packing.tileOrdinal(t);
        // must be a valid position in the sequence of tiles
        assert((ordinal >= 0 && ordinal < packing.tiles().cells()));
        // and the cell must be stored within its own tile's slab of storage: the offset lands
        // in the tile-sized window that starts where tile {ordinal} does
        assert((packing.offset(idx) >= ordinal * tileCells));
        assert((packing.offset(idx) < (ordinal + 1) * tileCells));
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> tile " << t << " @ " << ordinal
                << pyre::journal::newline;
    }
    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
