// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that injections work correctly in the absence of location information
int main() {
    // make a warning channel
    pyre::journal::warning_t channel("tests.journal.warning");

    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // do not provide location information
    channel
        << "a warning without location information"
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
