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


// exercise operator[]
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("order_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // make a constexpr index ordering
    constexpr order_t order_1 { 0, 1, 2, 3 };

    // show me
    channel
        << "[0,1,2,3]: " << order_1
        << pyre::journal::endl(__HERE__);

    // verify the contents are available at compile time
    static_assert (order_1[0] == 0);
    static_assert (order_1[1] == 1);
    static_assert (order_1[2] == 2);
    static_assert (order_1[3] == 3);

    // make a writable one
    order_t order_2 { 0,0,0,0 };

    // set it
    order_2[0] = 0;
    order_2[1] = 1;
    order_2[2] = 2;
    order_2[3] = 3;

    // show me
    channel
        << "[0,1,2,3]: " << order_2
        << pyre::journal::endl(__HERE__);

    // check it
    assert(( order_2[0] == 0 ));
    assert(( order_2[1] == 1 ));
    assert(( order_2[2] == 2 ));
    assert(( order_2[3] == 3 ));

    // all done
    return 0;
}


// end of file
