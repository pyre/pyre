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


// exercise the manipulators that control indentation level
int
main()
{
    // make an error channel
    myerror_t channel("tests.journal.error");

    // send the output to the trash
    channel.device<trash_t>();

    // carefully
    try {
        // inject something into the channel
        channel
            // location
            << pyre::journal::at(__HERE__)
            // some metadata
            << pyre::journal::note("time", "now")
            // a structured message
            << "top level"
            << pyre::journal::newline
            // level one
            << pyre::journal::indent << "level 1"
            << pyre::journal::newline
            // level 2
            << pyre::journal::indent << "level 2"
            << pyre::journal::newline
            // level 1
            << pyre::journal::outdent << "back to level 1"
            << pyre::journal::newline
            // top level
            << pyre::journal::outdent
            << "back to top level"
            // flush
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
