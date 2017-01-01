// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// configuration
#include <portinfo>
// externals
#include <numeric>
// support
#include <pyre/journal.h>
#include <pyre/memory.h>
#include <pyre/grid.h>

// main
int main() {
    // journal control
    // pyre::journal::debug_t debug("pyre.memory.direct");
    // debug.activate();

    // space
    typedef double cell_t;
    // shape
    typedef std::array<int, 3> rep_t;
    typedef pyre::grid::index_t<rep_t> index_t;
    typedef pyre::grid::order_t<rep_t> order_t;
    typedef pyre::grid::tile_t<index_t, order_t> tile_t;
    // convenience
    typedef pyre::memory::uri_t uri_t;
    // storage
    typedef pyre::memory::constdirect_t constdirect_t;
    // grid
    typedef pyre::grid::directgrid_t<cell_t, tile_t, constdirect_t> grid_t;

    // make an ordering
    tile_t::order_type order {2, 1, 0};
    // make a shape
    tile_t::index_type shape {6, 4, 5};
    // make a tile
    tile_t tile {shape, order};

    // the name of the file
    uri_t name {"grid.dat"};
    // map it and make the grid
    grid_t grid {name, tile};

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");
    // loop over the grid
    for (auto idx : grid.shape()) {
        // reduce the index
        auto v = std::accumulate(idx.begin(), idx.end(), 1, std::multiplies<cell_t>());
        // verify we read the correct value
        if (grid[idx] != v) {
            // make a channel
            pyre::journal::firewall_t firewall("pyre.grid");
            // show me
            firewall
                << pyre::journal::at(__HERE__)
                << "grid[" << idx << "] = " << grid[idx] << " != " << v
                << pyre::journal::endl;
            // and bail
            return 1;
        }
        // show me
        channel
            << pyre::journal::at(__HERE__)
            << "grid[" << idx << "] = " << grid[idx]
            << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
