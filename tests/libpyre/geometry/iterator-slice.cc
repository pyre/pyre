// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise looping through slices

// portability
#include <portinfo>
// support
#include <pyre/geometry.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 2> rep_t;
    // aliases
    typedef pyre::geometry::index_t<rep_t> index_t;
    typedef pyre::geometry::order_t<rep_t> order_t;
    typedef pyre::geometry::slice_t<index_t, order_t> slice_t;

    // make an ordering
    slice_t::order_type order {1, 0};
    // build the iteration boundaries
    slice_t::index_type low {0, 0};
    slice_t::index_type high {3, 2};
    // make a slice
    slice_t slice {low, high, order};

    // make a channel
    pyre::journal::debug_t channel("pyre.geometry");
    // sign in
    channel << pyre::journal::at(__HERE__);
    // loop through the slice
    for (auto cursor : slice) {
        // show me
        channel << "  (" << cursor << ")" << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
