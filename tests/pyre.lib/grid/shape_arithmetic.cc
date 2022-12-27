// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using shape_t = pyre::grid::shape_t<2>;


// shape arithmetic
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("shape_arithmetic");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // make a couple of shapes
    constexpr shape_t ref { 128, 128 };
    constexpr shape_t sec { 192, 192 };

    // make a shape out a combination of these
    shape_t cor = sec - ref + shape_t::fill(1);

    // show me
    channel
        << "ref: " << ref << pyre::journal::newline
        << "sec: " << sec << pyre::journal::newline
        << "cor: " << cor << pyre::journal::endl(__HERE__);

    // verify
    for (auto axis = 0; axis < shape_t::rank(); ++axis) {
        assert(( cor[axis] == sec[axis] - ref[axis] + 1 ));
    }

    // all done
    return 0;
}


// end of file
