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
#include <pyre/geometry.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 4> rep_t;
    // build the parts
    typedef pyre::geometry::index_t<rep_t> index_t;
    typedef pyre::geometry::layout_t<rep_t> layout_t;
    typedef pyre::geometry::tile_t<index_t, layout_t> tile_t;

    // make a layout
    tile_t::layout_type layout {3, 2, 1, 0};
    // make a shape
    tile_t::index_type shape {2, 3, 4, 5};
    // make a tile
    tile_t tile {shape, layout};
    // make a slice
    tile_t::slice_type slice = tile.slice({0,1,2,3});

    // make a channel
    pyre::journal::debug_t channel("pyre.geometry");

    // display information about the tile shape and layout
    channel
        << pyre::journal::at(__HERE__)
        << "low: (" << slice.low() << ")" << pyre::journal::newline
        << "high: (" << slice.high() << ")" << pyre::journal::newline
        << "layout: (" << slice.layout() << ")"
        << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
