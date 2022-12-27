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


// exercise iterating through the index contents
int main() {
    // make an index
    index_t index(true, true);

    // lookup a name
    index.lookup("test.index.1");
    // and another one
    index.lookup("test.index.2");

    // initialize the count
    std::size_t count = 0;
    // go through the contents
    for (auto & [key, inventory] : index) {
        // verify the channel activation state is as expected
        assert(inventory.active() == index.active());
        // verify the channel fatal state is as expected
        assert(inventory.fatal() == index.fatal());
        // increment the counter
        count++;
    }
    // verify that we went through all the channels
    assert(count == index.size());

    // all done
    return 0;
}


// end of file
