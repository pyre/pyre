// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise the common use case
int main() {
    // make a warning channel
    pyre::journal::warning_t channel("tests.journal.warning");

    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // inject something into the channel
    channel
        << pyre::journal::at(__HERE__)
        << pyre::journal::note("time", "now")
        << "warning channel:" << pyre::journal::newline
        << "    hello world!" << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
