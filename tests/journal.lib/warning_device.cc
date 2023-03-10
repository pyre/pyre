// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using file_t = pyre::journal::file_t;
using warning_t = pyre::journal::warning_t;


// send all output to a log file
int
main()
{
    // make a channel
    warning_t channel("tests.journal.warning");
    // and attach a logfile as its device, opened in append mode
    // note that ios_base::out is masked into the mode argument by default
    channel.device<file_t>("warning_device.log", std::ios_base::app);

    // inject something into the channel; there should be no output to the screen
    channel
        // some metadata
        << pyre::journal::note("time", "now")
        // a message with a newline
        << "warning channel:"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // another message
        << "hello world!"
        << pyre::journal::newline
        // and a flush with location warningrmation
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
