// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
//


// for the build system
#include <portinfo>

// packages
#include <cassert>
// access to the journal header file
#include <pyre/journal.h>

// main program
int main() {

    // instantiate a info channel
    pyre::journal::info_t info("pyre.journal.test");
    // check that it is inactive, by default
    assert(info.isActive() == false);

    // activate it
    info.activate();
    // and check
    assert(info.isActive() == true);

    // now, instantiate again using the same channel name
    pyre::journal::info_t again("pyre.journal.test");
    // check that it is active
    assert(again.isActive() == true);

    // all done
    return 0;
}

// end of file
