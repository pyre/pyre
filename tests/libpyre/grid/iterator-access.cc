// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// exercise iterator dereferencing

// portability
#include <portinfo>
// support
#include <pyre/grid.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 4> rep_t;
    // alias index and order
    typedef pyre::grid::index_t<rep_t> index_t;
    typedef pyre::grid::order_t<rep_t> order_t;
    typedef pyre::grid::slice_t<index_t, order_t> slice_t;
    // create a shortcut to my target iterator type
    typedef pyre::grid::iterator_t<slice_t> iterator_t;

    // make an ordering
    slice_t::order_type order {2, 3, 1, 0};
    // make a lower bound
    slice_t::index_type low {0, 0, 0, 0};
    // make an upper bound
    slice_t::index_type high {2, 3, 4, 5};
    // make a slice
    slice_t slice {low, high, order};

    // make an iterator
    iterator_t iterator {low, slice};

    // increment
    ++iterator;
    // get the value
    index_t got = *iterator;
    // here is what i expect
    index_t correct {0, 0, 1, 0};

    // check
    if (got != correct) {
        // make a firewall
        pyre::journal::firewall_t channel("pyre.grid");

        // sign in
        channel
            << pyre::journal::at(__HERE__)
            << "error while incrementing iterator:" << pyre::journal::newline
            // show me what i expected
            << "    expected: (" << correct << ")" << pyre::journal::newline
            // show me what i got
            << "    got: (" << got << ")" << pyre::journal::endl;

        // fail
        return 1;
    }

    // all done
    return 0;
}

// end of file
