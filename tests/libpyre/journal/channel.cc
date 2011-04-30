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
#include <map>
#include <string>
#include <cstdlib>

// access to the low level state header file
#include <pyre/journal/State.h>
#include <pyre/journal/Index.h>
#include <pyre/journal/Channel.h>

// convenience
// channel
typedef pyre::journal::Channel<false> channel_t;

// main program
int main() {
    //
    channel_t debug("pyre.journal.test");

    // all done
    return 0;
}

// end of file
