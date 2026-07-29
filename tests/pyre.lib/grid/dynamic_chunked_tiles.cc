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


// verify that the runtime rank flavor of {tilesOverlapping} finds the same working set as the
// compile time one
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dynamic_chunked_tiles");

    // describe a large product; a layout is pure arithmetic, so this costs nothing
    constexpr chunked_t oracle { shape_t { 100, 100 }, shape_t { 10, 10 } };
    // and its runtime twin
    const dynamic_t packing { { 100, 100 }, { 10, 10 } };

    // an algorithm's working window, deliberately not aligned with the tiles
    constexpr index_t base { 35, 42 };
    constexpr shape_t extent { 20, 20 };
    // find the tiles the window touches, the compile time way
    constexpr auto expected = pyre::grid::tilesOverlapping(oracle, base, extent);
    // and the runtime way
    const auto touched = pyre::grid::tilesOverlapping(packing, { 35, 42 }, { 20, 20 });

    // the two answers must name the same box in tile space: same first tile
    assert((touched.origin() == dynamic_t::index_type { 3, 4 }));
    assert((expected.origin() == index_t { 3, 4 }));
    // the same span of tiles
    assert((touched.shape() == dynamic_t::shape_type { 3, 3 }));
    assert((expected.shape() == shape_t { 3, 3 }));
    // and therefore the same working set
    assert((touched.cells() == expected.cells()));

    // the answer is itself a layout, so iterating it visits the working set; count the visits
    int visited = 0;
    // go through the touched tiles
    for (const auto & t : touched) {
        // each one must land inside the tile grid
        assert((t[0] >= 0 && t[0] < packing.tiles()[0]));
        assert((t[1] >= 0 && t[1] < packing.tiles()[1]));
        // and count it
        ++visited;
    }
    // the sweep must cover the working set exactly
    assert((visited == touched.cells()));

    // all done
    return 0;
}


// end of file
