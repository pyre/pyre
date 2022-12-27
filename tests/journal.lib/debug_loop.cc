// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using debug_t = pyre::journal::debug_t;
using trash_t = pyre::journal::trash_t;


// verify that repeated injection work correctly
int main() {
    // make a debug channel
    debug_t channel("tests.journal.debug");

    // activate the channel
    channel.activate();
    // send the output to the trash
    channel.device<trash_t>();

    // inject repeatedly
    for (auto i=0; i<10; ++i) {
        channel << "i: " << i << pyre::journal::endl;
    }

    // all done
    return 0;
}


// end of file
