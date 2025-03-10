// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>
// get the cuda memory support
#include <pyre/cuda/memory.h>


// verify the layout of a grid on the heap
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_managed_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.managed");

    // we'll work with a 3d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<3>;
    // of doubles on the heap
    using storage_t = pyre::cuda::memory::managed_t<double>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // packing: 1024x1024x8
    pack_t packing { { 1024, 1024, 8 } };
    // instantiate the grid
    grid_t grid { packing, packing.cells() };

    // show me
    channel << "value: " << sizeof(grid_t::value_type) << " bytes, "
            << "spacing: " << (&grid[{ 0, 0, 1 }] - &grid[{ 0, 0, 0 }]) << " cell, "
            << "spacing: " << (&grid[1] - &grid[0]) << " cell" << pyre::journal::endl;

    // verify that the address of the second element is the same regardless of the way it is
    // computed
    assert((&grid[{ 0, 0, 1 }] == &grid[1]));
    // verify that the distance between consecutive entries is precisely one cell
    assert(((&grid[{ 0, 0, 1 }] - &grid[{ 0, 0, 0 }]) == 1));

    // all done
    return 0;
}


// end of file
