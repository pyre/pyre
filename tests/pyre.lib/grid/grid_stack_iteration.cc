// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


#include <iostream>
// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// verify the layout of a grid on the stack
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_stack_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.stack");

    //  the space dimension
    const int dim = 3;
    // my cell
    using cell_t = double;
    // we'll work with a 3d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<3>;
    // of doubles on the stack
    using storage_t = pyre::memory::stack_t<dim * dim * dim, cell_t>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // packing: dim x dim x dim
    pack_t packing { { dim, dim, dim } };
    // instantiate the grid
    grid_t grid { packing };

    // fill it
    for (auto & value : grid) {
        // with some value
        value = 47;
    }

    // show me the value at the origin
    channel << "grid[0,0,0] = " << grid[{ 0, 0, 0 }] << pyre::journal::endl(__HERE__);

    // verify
    for (const auto & value : grid) {
        // that we have what we expect
        assert((value == 47));
    }

    // all done
    return 0;
}


// end of file
