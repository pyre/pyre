// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that flushing the channel resets its buffers correctly
int main() {
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");
    // activate it
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // try injecting something into the channel
    channel
        << pyre::journal::note("application", "debug_flush")
        << pyre::journal::note("time", "now")
        << "    hello world!"
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
