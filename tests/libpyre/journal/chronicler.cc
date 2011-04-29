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

    // request a key that is not there
    bool & state = chronicler.getChannelState("debug", "test");
    // verify that this is off by default
    assert(state == false);
    // turn it on
    state = true;

    // ask for it again, this time read only
    bool again = chronicler.getChannelState("debug", "test");
    // verify that it is now on
    assert(again == true);

    // all done
    return 0;
}

// end of file
