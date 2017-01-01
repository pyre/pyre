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
    // types for the mosaic cells, which are themselves grids
    // space
    typedef double cell_t;
    // shape
    typedef std::array<int, 3> crep_t;
    typedef pyre::grid::index_t<crep_t> cindex_t;
    typedef pyre::grid::order_t<crep_t> corder_t;
    typedef pyre::grid::tile_t<cindex_t, corder_t> ctile_t;
    // storage
    typedef pyre::memory::heap_t heap_t;
    // grid
    typedef pyre::grid::grid_t<cell_t, ctile_t, heap_t> grid_t;

    // types for the mosaic itself
    // shape
    typedef std::array<int, 2> mrep_t; // the mosaic is a 2d arrangement
    typedef pyre::grid::index_t<mrep_t> mindex_t;
    typedef pyre::grid::order_t<mrep_t> morder_t;
    typedef pyre::grid::tile_t<mindex_t, morder_t> mtile_t;
    // mosaic
    typedef pyre::grid::grid_t<grid_t, mtile_t, heap_t> mosaic_t;

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");

    // setup the shape of the mosaic
    mtile_t mtile { {2,2} };
    // setup the shape of the cell grids
    ctile_t ctile { {3,3,3}, {2,1,0} };

    // instantiate the mosaic
    mosaic_t mosaic {mtile};
    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "mosaic:" << pyre::journal::newline
        << "  shape: " << mosaic.shape()
        << pyre::journal::endl;

    // initialize the mosaic cells by going through each of its cells
    for (auto idx : mosaic.shape()) {
        // getting the address of the current one
        grid_t * current = &mosaic[idx];
        // and placing a new grid there
        new (current) grid_t(ctile);
    }

    // show me
    channel << pyre::journal::at(__HERE__);
    // the contents of each cell
    for (auto idx : mosaic.shape()) {
        channel
            << "mosaic[" << idx << "]: "
            << mosaic[idx].shape() << " at " << &mosaic[idx]
            << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl;

    // clean up
    for (auto idx : mosaic.shape()) {
        // invoke the destructor explicitly
        mosaic[idx].~grid_t();
    }

    // all done
    return 0;
}


// end of file
