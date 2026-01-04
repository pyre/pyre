// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise the channel manipulators
int
main()
{
    // make an debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // send the message to the trash
    channel.device<pyre::journal::trash_t>();

    // set the level of decoration
    pyre::journal::chronicler_t::decor(3);

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
        << "debug channel:"
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

    // all done
    return 0;
}


// end of file
