// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// exercise grid layout construction:
//   verify that all the parts are accessible through the public headers
//   verify constructor signatures
//   assemble a layout
//   verify it can be iterated

// portability
#include <portinfo>
// support
#include <pyre/geometry.h>

// entry point
int main() {
    // fix the rep
    typedef std::array<int, 4> rep_t;
    // alias index and layout
    typedef pyre::geometry::index_t<rep_t> index_t;
    typedef pyre::geometry::layout_t<rep_t> layout_t;
    // create a shortcut to my target iterator type
    typedef pyre::geometry::iterator_t<index_t, layout_t> iterator_t;

    // make a layout
    layout_t layout {3, 2, 1, 0};
    // build the iteration boundaries
    index_t begin {0, 0, 0, 0};
    index_t end {5, 4, 3, 2};
    // make a iterator
    iterator_t iterator {begin, end, layout};

    // all done
    return 0;
}

// end of file
