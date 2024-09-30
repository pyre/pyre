// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using trash_t = pyre::journal::trash_t;
using myerror_t = pyre::journal::error_t;


// exercise the channel manipulators
int
main()
{
    // make an error channel
    myerror_t channel("tests.journal.error");

    // send the message to the trash
    channel.device<trash_t>();

    // set the level of decoration
    pyre::journal::chronicler_t::decor(3);

    // carefully
    try {
        // inject something into the channel
        channel
#if defined(__cpp_lib_source_location)
            //  location
            << pyre::journal::here()
#else
            << pyre::journal::at(__HERE__)
#endif
            // some metadata
            << pyre::journal::note("time", "now")
            // sign on
            << "error channel:"
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // a message
            << "hello world!"
            << pyre::journal::newline
            // outdent
            << pyre::journal::outdent
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
