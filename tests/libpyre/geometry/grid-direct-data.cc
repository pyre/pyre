// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// configuration
#include <portinfo>
// externals
#include <iostream>
#include <pyre/journal.h>
#include <pyre/memory.h>
#include <pyre/geometry.h>

// main
int main() {
    // journal control
    // pyre::journal::debug_t debug("pyre.memory.direct");
    // debug.activate();

    // space
    typedef double cell_t;
    // shape
    typedef std::array<int, 3> rep_t;
    typedef pyre::geometry::index_t<rep_t> index_t;
    typedef pyre::geometry::order_t<rep_t> order_t;
    typedef pyre::geometry::tile_t<index_t, order_t> tile_t;
    // storage
    typedef pyre::memory::constdirect_t constdirect_t;
    // convenience
    typedef pyre::memory::uri_t uri_t;
    // grid
    typedef pyre::geometry::directgrid_t<cell_t, tile_t, constdirect_t> grid_t;

    // make a channel
    pyre::journal::debug_t channel("pyre.geometry");

    // make a shape
    tile_t::index_type shape {6, 4, 5};
    // make an ordering
    tile_t::order_type order {2, 1, 0};
    // make a tile
    tile_t tile {shape, order};

    // the name of the file
    uri_t name {"grid.dat"};
    // create it, map it, and make the grid
    grid_t grid {name, tile};

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "grid:" << pyre::journal::newline
        << "   shape: (" << grid.shape().shape() << ")" << pyre::journal::newline
        << "   order: (" << grid.shape().order() << ")" << pyre::journal::newline
        << "  mapped: " << grid.data()
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
