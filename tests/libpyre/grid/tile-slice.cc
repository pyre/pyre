// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise tile construction
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   verify tiles can be sliced

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

    // specify the slice region
    index_t begin {1,1,1,1};
    index_t end = tile.shape();

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");
    // if the channel is not active
    if (!channel) {
        // we are done
        return 0;
    }

    // otherwise, sign in
    channel << pyre::journal::at(__HERE__);

    // loop over the tile in packing order
    for (auto index : tile.slice(begin, end)) {
        // get the offset of the pixel at this index
        auto pixel = tile[index];
        // show me
        channel << "(" << index << ") -> " << pixel << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
