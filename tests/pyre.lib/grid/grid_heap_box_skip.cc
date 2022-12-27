// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// verify the layout of a grid on the heap
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_heap_box");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.heap");

    // we'll work with a 2d conventionally packed grid
    using layout_t = pyre::grid::canonical_t<2>;
    // of doubles on the heap
    using storage_t = pyre::memory::heap_t<double>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<layout_t, storage_t>;

    // make a shape
    layout_t::shape_type shape { 16, 16 };
    // turn into a layout
    layout_t layout { shape };
    // instantiate the grid
    grid_t grid { layout, layout.cells() };

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
    layout_t::index_type step { 4, 4 };

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
