// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>


// exercise all manipulators
int main() {
    // make a null channel
    pyre::journal::null_t channel("tests.journal.null");

    // inject the manipulators
    channel
        << pyre::journal::at(__HERE__)
        << pyre::journal::note("time", "now")
        << "null channel:" << pyre::journal::newline
        << "    Hello world!"
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
