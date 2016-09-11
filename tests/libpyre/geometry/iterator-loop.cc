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
    typedef std::array<int, 2> rep_t;
    // alias index; exercise the compiler's ability to deduce the layout
    typedef pyre::geometry::index_t<rep_t> index_t;
    // create a shortcut to my target iterator type
    typedef pyre::geometry::iterator_t<index_t> iterator_t;

    // make a layout
    iterator_t::layout_type layout {1, 0};
    // build the iteration boundaries
    index_t begin {0, 0};
    index_t end {3, 2};
    // make a iterator
    iterator_t iterator {begin, end, layout};

    // make a channel
    pyre::journal::debug_t channel("pyre.geometry");
    // sign in
    channel << pyre::journal::at(__HERE__);
    // loop until the iterator reaches the end
    for (const auto & cursor = *iterator; cursor != end; ++iterator) {
        // show me
        channel << "  (" << cursor << ")" << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
