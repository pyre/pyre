// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise the manipulators that control indentation level
int
main()
{
    // make a warning channel
    pyre::journal::warning_t channel("tests.journal.warning");

    // send the output to the trash
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

    // all done
    return 0;
}


// end of file
