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
#include <iostream>
#include <pyre/journal.h>

// main program
int main() {

    // instantiate a debug channel
    pyre::journal::debug_t debug("pyre.journal.test");

    // inject all the standard manipulators
    debug << pyre::journal::newline;
    debug << pyre::journal::endl;
    debug << pyre::journal::at(__HERE__);
    debug << pyre::journal::set("key", "value");

    // make sure injection of built in types works;
    debug << "Hello world!";

    // all done
    return 0;
}

// end of file
