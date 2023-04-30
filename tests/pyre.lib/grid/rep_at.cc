// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the grid
#include <pyre/grid.h>


// alias the rep
using rep_t = pyre::grid::rep_t<int, 4>;


// bounds safe data access
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("rep_at");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.rep");

    // make a rep
    constexpr rep_t rep { 0, 1, 2, 3 };
    // verify the contents
    static_assert (rep.at(0) == 0);

    // show me
    channel
        << "rep: {" << rep << "}"
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
