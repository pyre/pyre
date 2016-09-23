// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise slice construction
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   instantiate and access the simple interface

// portability
#include <portinfo>
// support
#include <pyre/grid.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 4> rep_t;
    // build the parts
    typedef pyre::grid::index_t<rep_t> index_t;
    typedef pyre::grid::order_t<rep_t> order_t;
    typedef pyre::grid::slice_t<index_t, order_t> slice_t;

    // make an ordering
    slice_t::order_type order {3, 2, 1, 0};
    // make a lower bound
    slice_t::index_type low {0, 0, 0, 0};
    // make an upper bound
    slice_t::index_type high {2, 3, 4, 5};
    // make a slice
    slice_t slice {low, high, order};

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");

    // display information about the tile shape and order
    channel
        << pyre::journal::at(__HERE__)
        << "low: (" << slice.low() << ")" << pyre::journal::newline
        << "high: (" << slice.high() << ")" << pyre::journal::newline
        << "order: (" << slice.order() << ")"
        << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
