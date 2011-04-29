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
// access to the packages used by Chronicler
#include <map>
#include <string>
#include <cstdlib>

// access to the low level header files
#include <pyre/journal/Index.h>
#include <pyre/journal/Chronicler.h>

// convenience
typedef pyre::journal::Chronicler chronicler_t;

// main program
int main() {

    // instantiate a chronicler
    chronicler_t chronicler;

    // request a couple of keys that are known to be present, as a result of the environment
    // variable setting in the makefile invocation
    chronicler_t::state_t test1 = chronicler.getChannelState("debug", "pyre.journal.test1");
    chronicler_t::state_t test2 = chronicler.getChannelState("debug", "pyre.journal.test2");
    // verify that they are activated
    assert(test1 == true);
    assert(test2 == true);

    // all done
    return 0;
}

// end of file
