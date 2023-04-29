// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// alias the rep
using rep_t = pyre::grid::rep_t<int, 5>;


// make a {rep} that's filled with zeroes
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("rep_fill");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.rep");

    // make up a value
    rep_t::value_type v = 42;
    // make a rep
    rep_t rep = rep_t::fill(v);

    // check that every entry
    for (auto rank : rep) {
        // is zero
        assert(( rank == v ));
    }

    // show me
    channel
        << "rep: {" << rep << "}"
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
