// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// get the journal
#include <pyre/journal.h>


// exercise all manipulators
int
main()
{
    // make a null channel
    pyre::journal::null_t channel("tests.journal.null");

    // inject the manipulators
    channel
        // location
        << pyre::journal::at(__HERE__)
        // notes
        << pyre::journal::note("time", "now")
        // message
        << "null channel:"
        // new line
        << pyre::journal::newline
        // indent two ways
        << pyre::journal::indent
        << pyre::journal::indent(2)
        // more message
        << "    Hello world!"
        // outdent two ways
        << pyre::journal::outdent(2)
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
