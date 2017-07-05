// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// configuration
#include <portinfo>
// externals
#include <iostream>
#include <pyre/journal.h>
#include <pyre/memory.h>
#include <pyre/grid.h>

// main
int main() {
    // journal control
    pyre::journal::debug_t debug("pyre.memory.direct");
    // debug.activate();

    // space
    typedef double cell_t;
    // shape
    typedef std::array<int, 3> rep_t;
    typedef pyre::grid::index_t<rep_t> index_t;
    typedef pyre::grid::packing_t<rep_t> packing_t;
    typedef pyre::grid::tile_t<index_t, packing_t> tile_t;
    // storage
    typedef pyre::memory::view_t view_t;
    // grid
    typedef pyre::grid::grid_t<cell_t, tile_t, view_t> grid_t;

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");

    // make an ordering
    tile_t::packing_type packing {2, 1, 0};
    // make a shape
    tile_t::index_type shape {6, 4, 2};
    // make a tile
    tile_t tile {shape, packing};

    // allocate some memory
    cell_t * buffer = new cell_t[tile.size()];
    // initialize the memory with predictable values
    for (tile_t::size_type i=0; i<tile.size(); ++i) {
        buffer[i] = i;
    }

    // make grid
    // N.B.: {buffer} is auto-converted into a view by the grid constructor
    grid_t grid {tile, buffer};

    // loop over the grid
    for (auto idx : grid.shape()) {
        // get the value stored at this location
        auto value = grid[idx];
        // the expected value is the current offset as a double
        grid_t::cell_type expected = grid.shape().offset(idx);
        // if they are not the same
        if (value != expected) {
            // make a channel
            pyre::journal::firewall_t firewall("pyre.grid");
            // show me
            firewall
                << pyre::journal::at(__HERE__)
                << "grid[" << idx << "]: " << value << " != " << expected
                << pyre::journal::endl;
            // and bail
            return 1;
        }
    }

    // clean up
    delete [] buffer;
    // all done
    return 0;
}


// end of file
