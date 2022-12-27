// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// alias the rep
using shape_t = pyre::grid::shape_t<3>;


// verify that structured bindings work
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("shape_structured_binding");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // make a rep
    shape_t shape { 10, 20, 30 };
    // unpack it
    auto [x, y, z] = shape;

    // show me
    channel
        << "shape: {" << shape << "}" << pyre::journal::newline
        << "unpacked: {" << x << ", " << y << ", " << z << "}"
        << pyre::journal::endl(__HERE__);

    // check
    assert(( x == shape[0] ));
    assert(( y == shape[1] ));
    assert(( z == shape[2] ));

    // all done
    return 0;
}


// end of file
