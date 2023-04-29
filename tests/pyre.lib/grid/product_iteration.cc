// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>

// type alias
using product_t = pyre::grid::product_t<4>;


// exercise iterating over products
int main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("product_iteration");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.product");

    // make one
    product_t p {0, 1, 2, 3};
    // show me
    channel
        << "product before: " << p
        << pyre::journal::endl(__HERE__);
    // fill
    for (auto & f : p) {
        // with a specific value
        f = 42;
    }
    // show me
    channel
        << "product after: " << p
        << pyre::journal::endl(__HERE__);

    // check
    for (const auto f : p) {
        // that we get what we expect
        assert(( f == 42 ));
    }

    // all done
    return 0;
}


// end of file
