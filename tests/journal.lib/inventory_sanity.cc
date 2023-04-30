// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// verify that we can instantiate and manipulate inventories


// get the journal
#include <pyre/journal.h>

// support
#include <cassert>


// convenience
using inventory_t = pyre::journal::inventory_t;


// verify that we can manipulate the inventory state
int main() {
    // make a default inventory
    inventory_t on(true, true);
    // verify it is on
    assert(on.active() == true);
    // flip it
    on.active(false);
    // check again
    assert(on.active() == false);
    // verify it is fatal
    assert(on.fatal() == true);
    // flip it
    on.fatal(false);
    // check again
    assert(on.fatal() == false);
    // by default, its device is null
    assert(on.device().get() == nullptr);

    // make one that is off by default
    inventory_t off(false, false);
    // verify it is off
    assert(off.active() == false);
    // flip it
    off.active(true);
    // check again
    assert(off.active() == true);
    // verify it is fatal
    assert(on.fatal() == false);
    // flip it
    on.fatal(true);
    // check again
    assert(on.fatal() == true);
    // by default, its device is null
    assert(off.device().get() == nullptr);

    // all done
    return 0;
}


// end of file
