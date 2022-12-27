// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type alias
using index_t = pyre::journal::index_t;


// verify that the channel state index can be instantiated
int main() {
    // make an index
    index_t index(true, true);

    // make sure it's empty
    assert(index.empty());

    // all done
    return 0;
}


// end of file
