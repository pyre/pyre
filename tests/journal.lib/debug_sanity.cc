// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that the debug diagnostic is off by default, and that we can manipulate its state
int main() {
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // check its name
    assert (channel.name() == "tests.journal.debug");
    // by default, it should be inactive
    assert (channel.active() == false);
    // and non-fatal
    assert (channel.fatal() == false);

    // all done
    return 0;
}


// end of file
