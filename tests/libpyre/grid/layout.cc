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
    // fix the representation
    typedef std::array<int, 4> rep_t;
    // alias
    typedef pyre::geometry::layout_t<rep_t> layout_t;
    // make the interleaving
    layout_t layout = {0, 1, 2, 3};

    // make a channel
    pyre::journal::debug_t channel("pyre.geometry");
    // and display information about the tile layout
    channel << pyre::journal::at(__HERE__) << "layout : (";
    // go through the values
    for (auto index : layout) {
        // inject them
        channel << " " << index;
    }
    // flush
    channel << " )" << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
