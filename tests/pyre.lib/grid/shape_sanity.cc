// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using shape_t = pyre::grid::shape_t<4>;


// sanity check
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("shape_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // make a shape
    constexpr shape_t s { 2, 3, 4, 5 };
    // show me
    channel
        << "s: " << s << pyre::journal::newline
        << "  rank: " << shape_t::rank() << "  (from the type)" << pyre::journal::newline
        << "  rank: " << s.rank() << "  (from the instance)" << pyre::journal::newline
        << "  cells: " << s.cells()
        << pyre::journal::endl(__HERE__);

    // verify that the index dimensionality is reported correctly through the type
    static_assert (shape_t::rank() == 4);
    // verify that the index dimensionality is reported correctly through an instance
    static_assert (s.rank() == 4);

    // verify that its capacity is equal to the product of the possible values along each axis
    assert(( s.cells() == 2*3*4*5 ));

    // verify that a shape is equal to itself
    assert(( s == s ));

    // make another
    shape_t z { 2, 3, 4, 5 };
    // that's equal to {s}
    assert(( s == z ));

    // all done
    return 0;
}


// end of file
