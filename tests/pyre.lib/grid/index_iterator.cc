// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using idx_t = pyre::grid::index_t<4>;


// exercise the filling constructor
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_iterator");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a const index
    constexpr idx_t idx { 0,1,2,3 };
    // show me
    channel
        << "idx: " << idx
        << pyre::journal::endl(__HERE__);

    // make a ounter
    int i = 0;
    // go through the index ranks
    for (auto value : idx) {
        // verify it is as expected
        assert(( value == i ));
        // get ready for the next one
        ++i;
    }

    // all done
    return 0;
}


// end of file
