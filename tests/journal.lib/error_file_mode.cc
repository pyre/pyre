// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using trash_t = pyre::journal::trash_t;
using myerror_t = pyre::journal::error_t;


// send all output to a log file
int
main()
{
    // send the errors to a log file
    myerror_t::logfile("error_file_mode.log", std::ios_base::app);

    // make an error channel
    myerror_t channel("tests.journal.error");

    // carefully
    try {
        // inject something into the channel
        channel << pyre::journal::at(__HERE__) << pyre::journal::note("time", "now")
                << "error channel:" << pyre::journal::newline << "    hello world!"
                << pyre::journal::endl;
        // errors are fatal by default, so we shouldn't be able to get here
        throw std::logic_error("unreachable");
        // if all goes well
    } catch (const myerror_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert(error.what() == channel.name() + myerror_t::string_type(": application error"));
    }

    // all done
    return 0;
}


// end of file
