// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise grid order construction:
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   assemble a order
//   verify it can be iterated

// portability
#include <portinfo>
// support
#include <pyre/geometry.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 4> rep_t;
    // alias index and order
    typedef pyre::geometry::index_t<rep_t> index_t;
    typedef pyre::geometry::order_t<rep_t> order_t;
    // create a shortcut to my target iterator type
    typedef pyre::geometry::iterator_t<index_t, order_t> iterator_t;

    // make a order
    order_t order {3, 2, 1, 0};
    // build the iteration boundaries
    index_t begin {0, 0, 0, 0};
    index_t end {5, 4, 3, 2};
    // make a iterator
    iterator_t iterator {begin, end, order};

    // all done
    return 0;
}

// end of file
