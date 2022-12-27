// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the journal
#include <pyre/journal.h>


// verify that the null diagnostic is always off
int main() {
    // make a null channel
    pyre::journal::null_t channel("tests.journal.null");

    // if it's active by default, we have a problem
    assert (!channel);

    // attempt to activate
    channel.activate();

    // if it activated, we have a problem
    assert (!channel);

    // nothing to do
    return 0;
}


// end of file
