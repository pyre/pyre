// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using warning_t = pyre::journal::warning_t;
using trash_t = pyre::journal::trash_t;


// exercise repeated injection into a warning channel
int main() {
    // make a warning channel
    warning_t channel("tests.journal.warning");

    // send the output to the trash
    channel.device<trash_t>();

    // inject repeatedly
    for (auto i=0; i<10; ++i) {
        channel << "i: " << i << pyre::journal::endl;
    }

    // all done
    return 0;
}


// end of file
