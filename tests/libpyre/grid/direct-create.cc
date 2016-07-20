// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// access the low level interface to create a file that can fit an grid of a specified size
//
// N.B.: this test leaves behind a file named "grid.dat" that is used by the other tests; it
// must be cleaned up after the tests are run

// portability
#include <portinfo>

// support
#include <pyre/grid.h>

// entry point
int main() {
    // units
    auto k = 1024;
    // declare the type of a pixel
    typedef double pixel_t;
    // fix the rep
    typedef std::array<int, 3> rep_t;
    // build the parts
    typedef pyre::grid::index_t<rep_t> index_t;
    typedef pyre::grid::layout_t<rep_t> layout_t;
    typedef pyre::grid::tile_t<index_t, layout_t> tile_t;

    // the name of the file
    pyre::grid::uri_t name {"grid.dat"};
    // make a layout
    tile_t::layout_type layout {2, 1, 0};
    // make a shape
    tile_t::index_type shape {1*k, 3*k, 3};
    // make a tile
    tile_t tile {shape, layout};

    // turn on the info channel
    // pyre::journal::debug_t("pyre.grid.direct").activate();
    // create a file that can fit the payload
    pyre::grid::direct_t::create(name, sizeof(pixel_t)*tile.size());

    // all done
    return 0;
}

// end of file
