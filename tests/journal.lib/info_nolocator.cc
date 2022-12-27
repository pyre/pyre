// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that injection happens correctly even in the absence of location information
int main() {
    // make an info channel
    pyre::journal::info_t channel("tests.journal.info");

    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // do not provide location information
    channel
        << "an informational message without location information"
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
