// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// verify the layout of a grid on the heap
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_heap_box");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.heap");

    // we'll work with a 3d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<3>;
    // of doubles on the heap
    using storage_t = pyre::memory::heap_t<double>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // packing
    pack_t packing { {3, 3, 3} };
    // instantiate the grid
    grid_t grid { packing, packing.cells() };

    // visit every location on the grid
    for (auto & cell : grid) {
        // and set it to zero
        cell = 0;
    }
    // show me
    channel << "grid before box:" << pyre::journal::newline;
    for (const auto & idx : grid.layout()) {
        channel << "  " << idx << " -> " << grid[idx] << pyre::journal::newline;
    }
    channel << pyre::journal::endl(__HERE__);

    // make a box that excludes the outer surfaces
    // top corner
    pack_t::index_type top = pack_t::index_type::one();
    // shape
    pack_t::shape_type interior = grid.layout().shape() - 2*pack_t::shape_type::one();
    // put them together to make the box
    auto box = grid.layout().box(top, interior);

    // set the values in the box
    for (auto & cell : grid.box(top, interior)) {
        // to one
        cell = 1;
    }

    // show me
    channel << "box:" << pyre::journal::newline;
    for (const auto & idx : box) {
        channel << "  " << idx << " -> " << grid[idx] << pyre::journal::newline;
    }
    channel << pyre::journal::endl(__HERE__);

    // show me
    channel << "grid after box:" << pyre::journal::newline;
    for (const auto & idx : grid.layout()) {
        channel << "  " << idx << " -> " << grid[idx] << pyre::journal::newline;
    }
    channel << pyre::journal::endl(__HERE__);

    // verify that the value at the center of the grid is one
    assert(( grid[{1,1,1}] == 1 ));
    // and the rest is all zeroes
    for (const auto & idx : grid.layout()) {
        if (idx == pack_t::index_type::one()) {
            continue;
        }
        assert(( grid[idx] == 0 ));
    }

    // all done
    return 0;
}


// end of file
