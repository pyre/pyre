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

    //  the grid dimension
    const int dim = 16;
    // my cell
    using cell_t = double;
    // we'll work with a 2d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<2>;
    // of doubles on the stack
    using storage_t = pyre::memory::stack_t<dim * dim, cell_t>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // packing: dim x dim x dim
    pack_t packing { { dim, dim } };
    // instantiate the grid
    grid_t grid { packing };

    // make a counter
    auto v = 0.0;
    // visit every location on the grid
    for (auto & cell : grid) {
        // set it
        cell = v;
        // and increment the value
        v += 1.0;
    }

    // set up a skip
    pack_t::index_type step { dim / 4, dim / 4 };

    // go through the grid, skipping every {step}
    for (auto i = grid.cbegin(step); i != grid.cend(); ++i) {
        // show me
        channel << *i << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
