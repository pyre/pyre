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
using myerror_t = pyre::journal::error_t;


// send all output to a log file
int
main()
{
    // make a channel
    myerror_t channel("tests.journal.error");
    // make sure it's not fatal
    channel.fatal(false);
    // and attach a logfile as its device, opened in append mode
    // note that ios_base::out is masked into the mode argument by default
    channel.device<file_t>("error_device.log", std::ios_base::app);

    // inject something into the channel; there should be no output to the screen
    channel
        // some metadata
        << pyre::journal::note("time", "now")
        // a message with a newline
        << "error channel:"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // another message
        << "hello world!"
        << pyre::journal::newline
        // and a flush with location information
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
