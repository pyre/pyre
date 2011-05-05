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

    // instantiate a debug channel
    pyre::journal::debug_t debug("pyre.journal.test");

    // inject all the standard manipulators
    debug
        << pyre::journal::at(__HERE__)
        << pyre::journal::set("key", "value")
        << pyre::journal::newline
        << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
