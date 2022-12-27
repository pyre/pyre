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


// exercise the channel state index
int main() {
    // make an index
    index_t index(true, true);

    // lookup a name
    auto & inventory = index.lookup("test.index");

    // make sure its activation state is what we expect
    assert(inventory.active() == true);
    // turn it off
    inventory.active(false);
    // make sure it happened
    assert(inventory.active() == false);

    // check whether it's fatal
    assert(inventory.fatal() == true);
    // turn it off
    inventory.fatal(false);
    // make sure it happened
    assert(inventory.fatal() == false);

    // the default device is a {nullptr}
    assert(inventory.device() == nullptr);

    // all done
    return 0;
}


// end of file
