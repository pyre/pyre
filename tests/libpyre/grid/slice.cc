// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise grid layout construction:
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   assemble a layout
//   verify it can be iterated

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
    typedef pyre::grid::layout_t<rep_t> layout_t;
    typedef pyre::grid::tile_t<index_t, layout_t> tile_t;

    // make a layout
    tile_t::layout_type layout {3, 2, 1, 0};
    // make a shape
    tile_t::index_type shape {2, 3, 4, 5};
    // make a tile
    tile_t tile {shape, layout};
    // make a slice
    tile_t::slice_type slice = tile.slice({0,1,2,3});

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");

    // display information about the tile layout
    channel << pyre::journal::at(__HERE__);

    // show me the shape
    channel << "shape: (";
    for (auto sz : slice.shape()) {
        channel << " " << sz;
    }
    channel << " )" << pyre::journal::endl;

    // show me the layout
    channel << "layout: (";
    for (auto sz : slice.layout()) {
        channel << " " << sz;
    }
    channel << " )" << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
