// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify we can suppress all channel output
int main() {
    // quiet {warning} channels by sending the output to a trash can
    pyre::journal::warning_t::quiet();

    // make a warning channel
    pyre::journal::warning_t channel("tests.journal.warning");

    // inject something into the channel; there should be no output to the screen
    channel
        // location
        << pyre::journal::at(__HERE__)
        // some metadata
        << pyre::journal::note("time", "now")
        // a message with a newline
        << "warning channel:" << pyre::journal::newline
        // another message and a flush
        << "    hello world!" << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
