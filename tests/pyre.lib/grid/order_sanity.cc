// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using order_t = pyre::grid::order_t<4>;


// sanity check
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("order_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // make an index ordering
    order_t shuffle { 0, 1, 2, 3 };

    // show me
    channel
        << "an ordering: " << shuffle << pyre::journal::newline
        << "  rank: " << order_t::rank() << "  (from the type)" << pyre::journal::newline
        << "  rank: " << shuffle.rank() << "  (from the instance)"
        << pyre::journal::endl(__HERE__);

    // verify that the dimensionality is reported correctly through the type
    static_assert (order_t::rank() == 4);
    // verify that the dimensionality is reported correctly through an instance
    static_assert (shuffle.rank() == 4);

    // make a column major ordering
    order_t fortran = order_t::fortran();
    // show me
    channel
        << "fortran: " << fortran
        << pyre::journal::endl(__HERE__);
    // check that it's equal to {shuffle}
    assert(( shuffle == fortran ));

    // make a column major ordering
    order_t c = order_t::c();
    // show me
    channel
        << "c: " << c
        << pyre::journal::endl(__HERE__);
    // check that it's different from {shuffle}
    assert(( shuffle != c ));

    // all done
    return 0;
}


// end of file
