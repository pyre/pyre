// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// exercise ranged for loops
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_heap_iteration");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.heap");

    // we'll work with a 3d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<3>;
    // of doubles on the heap
    using storage_t = pyre::memory::heap_t<double>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // packing: 1024x1024x8
    pack_t packing { {1024, 1024, 8} };
    // instantiate the grid
    grid_t grid { packing, packing.cells() };

    // fill it
    for (auto & value : grid) {
        // with some value
        value = 47;
    }

    // show me the value at the origin
    channel
        << "grid[0,0,0] = " << grid[{0,0,0}]
        << pyre::journal::endl(__HERE__);

    // verify
    for (const auto & value : grid) {
        // that we have what we expect
        assert(( value == 47 ));
    }

    // all done
    return 0;
}


// end of file
