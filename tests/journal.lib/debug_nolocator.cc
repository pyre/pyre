// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that everything works correctly in the absence of location information
int main() {
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // turn it on
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // do not provide location information
    channel
        << "a debug message without location information"
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
