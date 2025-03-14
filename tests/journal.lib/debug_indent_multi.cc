// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise the channel manipulators
int
main()
{
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // activate it
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

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
        << pyre::journal::indent(2) << "level 3"
        << pyre::journal::newline
        // level 2
        << pyre::journal::outdent << "back to level 2"
        << pyre::journal::newline
        // level 1
        << pyre::journal::outdent(2) << "back to top level"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
