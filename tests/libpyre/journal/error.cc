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
// access to the journal header file
#include <pyre/journal.h>

// main program
int main() {

    // instantiate a error channel
    pyre::journal::error_t error("pyre.journal.test");
    // check that it is inactive, by default
    assert(error.isActive() == true);

    // activate it
    error.deactivate();
    // and check
    assert(error.isActive() == false);

    // now, instantiate again using the same channel name
    pyre::journal::error_t again("pyre.journal.test");
    // check that it is active
    assert(again.isActive() == false);

    // all done
    return 0;
}

// end of file
