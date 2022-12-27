// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that empty messages are handled correctly
int main() {
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");
    // activate the channel
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // inject nothing
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
