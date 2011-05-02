// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


// for the build system
#include <portinfo>

// packages
#include <assert.h>

// access to the low level inventory header file
#include <pyre/journal/Inventory.h>
#include <pyre/journal/Channel.h>

// convenience
typedef pyre::journal::Inventory<true> true_t;
typedef pyre::journal::Inventory<false> false_t;

typedef pyre::journal::Channel<true> trueref_t;
typedef pyre::journal::Channel<false> falseref_t;

// main program
int main() {

    // instantiate a couple of inventories
    true_t on;
    false_t off;
    // and wrap channels over them
    trueref_t on_ref(on);
    falseref_t off_ref(off);

    // check their default settings
    assert(on_ref.isActive() == true);
    assert(off_ref.isActive() == false);

    // flip them
    on_ref.deactivate();
    off_ref.activate();

    // check again
    assert(on_ref.isActive() == false);
    assert(off_ref.isActive() == true);

    // all done
    return 0;
}

// end of file
