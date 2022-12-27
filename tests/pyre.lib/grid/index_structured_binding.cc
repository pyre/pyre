// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// alias the rep
using index_t = pyre::grid::index_t<3>;


// verify that structured bindings work
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_structured_binding");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a rep
    index_t idx { 10, 20, 30 };
    // unpack it
    auto [x, y, z] = idx;

    // show me
    channel
        << "idx: {" << idx << "}" << pyre::journal::newline
        << "unpacked: {" << x << ", " << y << ", " << z << "}"
        << pyre::journal::endl(__HERE__);

    // check
    assert(( x == idx[0] ));
    assert(( y == idx[1] ));
    assert(( z == idx[2] ));

    // all done
    return 0;
}


// end of file
