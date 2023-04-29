// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// verify the basic layout of memory mapped grids
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_mmap_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.mmap");

    // we'll work with a 3d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<3>;
    // of doubles on the heap
    using storage_t = pyre::memory::map_t<double>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // packing: 1024x1024x8
    pack_t packing { {1024,1024, 8} };
    // instantiate the grid
    grid_t grid { packing, "grid_mmap.data", packing.cells() };

    // make an index
    grid_t::index_type zero {};
    // set a value
    grid[zero] = 42;
    // show me the value
    channel
        << "grid[0,0,0] = " << grid[{0,0,0}]
        << pyre::journal::endl(__HERE__);

    // check
    assert(( grid[zero] == 42 ));

    // all done
    return 0;
}


// end of file
