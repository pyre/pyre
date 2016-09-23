// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise grid order construction:
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   assemble an ordering
//   verify it can be iterated

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
    // instantiate an ordering
    order_t order = {0, 1, 2, 3};

    // make a firewall
    pyre::journal::firewall_t channel("pyre.grid");

    // check the values one by one
    for (order_t::size_type i=0; i < order.size(); ++i) {
        // check this one
        if (order[i] != static_cast<order_t::value_type>(i)) {
            // complain
            channel
                << pyre::journal::at(__HERE__)
                << "index mismatch: " << order[i] << " != " << i
                << pyre::journal::endl;
            // and bail
            return 1;
        }
    }

    // all done
    return 0;
}

// end of file
