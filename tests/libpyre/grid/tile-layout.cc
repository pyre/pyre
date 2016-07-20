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

    // initialize the offset
    size_t offset = 0;

    // loop over the tile in packing order
    for (auto index : tile) {
        // get the offset of the pixel at this index
        auto pixel = tile[index];
        // verify it has the expected value
        if (offset != pixel) {
            // open a channel
            pyre::journal::firewall_t firewall("pyre.grid.index");
            // complain
            firewall
                << pyre::journal::at(__HERE__)
                << "offset error: " << offset << " != " << pixel
                << pyre::journal::endl;
            // and bail
            return 1;
        }

        // map the offset back to an index
        auto refl = tile[offset];
        // and verify it is identical to our loop index
        if (refl != index) {
            // open a channel
            pyre::journal::firewall_t firewall("pyre.grid.index");
            // complain
            firewall
                << pyre::journal::at(__HERE__)
                << "index error at offset " << offset << pyre::journal::newline
                << "(" << index[0] << "," << index[1] << "," << index[2] << ")"
                << " != "
                << "(" << refl[0] << "," << refl[1] << "," << refl[2] << ")"
                << pyre::journal::endl;
            // and bail
            return 1;
        }

        // update the counter
        offset++;
    }

    // all done
    return 0;
}

// end of file
