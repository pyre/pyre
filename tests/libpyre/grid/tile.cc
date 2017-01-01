// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// exercise tile construction:
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   exercise the simpel interface

// portability
#include <portinfo>
// support
#include <pyre/grid.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 4> rep_t;
    // build the parts
    typedef pyre::grid::index_t<rep_t> index_t;
    typedef pyre::grid::order_t<rep_t> order_t;
    typedef pyre::grid::tile_t<index_t, order_t> tile_t;

    // make an ordering
    tile_t::order_type order {3, 2, 1, 0};
    // make a shape
    tile_t::index_type shape {2, 3, 4, 5};
    // make a tile
    tile_t tile {shape, order};

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");

    // display information about the tile shape and order
    channel
        << pyre::journal::at(__HERE__)
        << "shape: (" << tile.shape() << ")" << pyre::journal::newline
        << "order: (" << tile.order() << ")" << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
