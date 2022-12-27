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


// send all output to a log file
int main() {
    // send all channel output to a log file
    pyre::journal::logfile("api_file.log");

    // make a debug channel
    debug_t channel("tests.journal.debug");
    // and activate it
    channel.activate();

    // inject something into the channel; there should be no output to the screen
    channel
        // location
        << pyre::journal::at(__HERE__)
        // some metadata
        << pyre::journal::note("time", "now")
        // a message with a newline
        << "debug channel:" << pyre::journal::newline
        // another message and a flush
        << "    hello world!" << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
