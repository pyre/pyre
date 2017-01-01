// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// exercise grid order construction:
//   verify that all the parts are accessible through the public headers
//   assemble a C style ordering
//   verify it can be injected into a stream

// portability
#include <portinfo>
// support
#include <pyre/grid.h>

// entry point
int main() {
    // fix the representation
    typedef std::array<int, 4> rep_t;
    // alias
    typedef pyre::grid::order_t<rep_t> order_t;
    // make a C-style interleaving
    order_t order = order_t::rowMajor();

    // go through the order contents
    for (order_t::size_type i=0; i<order.size(); ++i) {
        // we expect
        order_t::value_type expected = order.size() - i - 1;
        // and check that it is sorted in descending order
        if (order[i] != expected) {
            // make a firewall
            pyre::journal::firewall_t channel("pyre.grid");
            // complain
            channel
                << pyre::journal::at(__HERE__)
                << "order mismatch at " << i << ": " << order[i] << " != " << expected
                << pyre::journal::endl;
            // and bail
            return 1;
        }
    }

    // make a channel
    pyre::journal::debug_t channel("pyre.grid");
    // and display information about the tile order
    channel
        << pyre::journal::at(__HERE__)
        << "order : (" << order << ")"
        << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
