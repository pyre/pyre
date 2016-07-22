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
    // alias index; exercise the compiler's ability to deduce the layout
    typedef pyre::geometry::index_t<rep_t> index_t;
    // create a shortcut to my target iterator type
    typedef pyre::geometry::iterator_t<index_t> iterator_t;

    // make a layout
    iterator_t::layout_type layout {2, 3, 1, 0};
    // build the iteration boundaries
    index_t begin {0, 0, 0, 0};
    index_t end {5, 4, 3, 2};
    // make a iterator
    iterator_t iterator {begin, end, layout};

    // increment
    ++iterator;
    // get the value
    index_t got = *iterator;
    // here is what i expect
    index_t correct {0, 0, 1, 0};

    // check
    if (got != correct) {
        // make a firewall
        pyre::journal::firewall_t channel("pyre.geometry");

        // sign in
        channel
            << pyre::journal::at(__HERE__)
            << "error while incrementing iterator:"
            << pyre::journal::newline;
        // show me what i expected
        channel << "expected: (";
        for (auto idx : correct) {
            channel << " " << idx;
        }
        channel << " )" << pyre::journal::newline;
        // show me what i got
        channel << "     got: (";
        for (auto idx : got) {
            channel << " " << idx;
        }
        channel << " )" << pyre::journal::endl;

        // fail
        return 1;
    }

    // all done
    return 0;
}

// end of file
