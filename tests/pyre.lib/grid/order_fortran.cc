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
    pyre::journal::application("order_fortran");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // make a constexpr column major index ordering
    constexpr order_t columnMajor = order_t::fortran();

    // show me
    channel
        << "column major: " << columnMajor
        << pyre::journal::endl(__HERE__);

    // verify the contents are accessible at compile time
    static_assert (columnMajor[0] == 0);
    static_assert (columnMajor[1] == 1);
    static_assert (columnMajor[2] == 2);
    static_assert (columnMajor[3] == 3);

    // all done
    return 0;
}


// end of file
