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
    pyre::journal::application("rep_eq");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.rep");

    // make a rep full of zeroes
    constexpr rep_t rep1 {};
    // and another
    constexpr auto repyre = rep_t::zero();

    // verify they are equal
    assert(( rep1 == repyre ));

    // show me
    channel
        << "rep1: {" << rep1 << "}"
        << "repyre: {" << repyre << "}"
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
