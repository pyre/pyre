// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the grid
#include <pyre/grid.h>


// type alias
using order_t = pyre::grid::order_t<4>;


// exercise operator[]
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("order_c");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // make a constexpr row major index ordering
    constexpr order_t rowMajor = order_t::c();

    // show me
    channel
        << "row major: " << rowMajor
        << pyre::journal::endl(__HERE__);

    // verify the contents are accessible at compile time
    static_assert (rowMajor[0] == 3);
    static_assert (rowMajor[1] == 2);
    static_assert (rowMajor[2] == 1);
    static_assert (rowMajor[3] == 0);

    // all done
    return 0;
}


// end of file
