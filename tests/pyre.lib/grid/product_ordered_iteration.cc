// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>

// type aliases
using order_t = pyre::grid::order_t<4>;
using product_t = pyre::grid::product_t<4>;


// exercise iterating over products
int main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("product_ordered_iteration");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.product");

    // make one
    constexpr product_t product { 3, 0, 2, 1 };
    // the order that sorts it
    constexpr order_t order { 1, 3, 2, 0 };

    // show me
    channel
        << "product in normal order: " << product
        << pyre::journal::endl(__HERE__);

    // make a counter
    product_t::value_type i = 0;
    // sign in
    channel << "product in ascending order: ";
    // now, in sorted order
    for (auto it = product.begin(order); it != product.end(order); ++it) {
        // check that we are visiting in sorted order
        assert(( *it == i ));
        // show me
        channel << *it << " ";
        // update the counter
        ++i;
    }
    // flush
    channel << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
