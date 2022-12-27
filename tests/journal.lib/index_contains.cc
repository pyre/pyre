// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using index_t = pyre::journal::index_t;


// verify that looking up channel names in the index creates nodes
int main() {
    // make an index
    index_t index(true, true);

    // lookup a couple of names
    index.lookup("test.index.1");
    index.lookup("test.index.2");

    // make sure the index contains two names
    assert (index.size() == 2);
    // and that out names are the ones there
    assert (index.contains("test.index.1"));
    assert (index.contains("test.index.2"));

    // all done
    return 0;
}


// end of file
