// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// make sure empty injections into a warning work as expected
int main() {
    // make a warning channel
    pyre::journal::warning_t channel("tests.journal.warning");
    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // inject nothing
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
