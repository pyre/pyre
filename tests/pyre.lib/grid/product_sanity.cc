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

// exercise the basic {product_t} interface
int main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("product_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.product");

    // make an index
    product_t p { 0, 0, 0, 0 };
    // show me
    channel
        << "product: " << p << pyre::journal::newline
        << "  rank: " << product_t::rank() << "  (from the type)" << pyre::journal::newline
        << "  rank: " << p.rank() << "  (from the instance)"
        << pyre::journal::endl(__HERE__);

    // verify that the index dimensionality is reported correctly through the type
    static_assert( product_t::rank() == 4 );
    // verify that the index dimensionality is reported correctly through an instance
    static_assert( p.rank() == 4 );

    // every product is equal to itself
    assert(( p == p ));

    // make a different one
    product_t q { 1, 1, 1, 1 };
    // verify it's not the same as {q}
    assert(( p != q ));

    // all done
    return 0;
}


// end of file
