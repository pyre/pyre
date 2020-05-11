// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// get the journal
#include <pyre/journal.h>


// verify that the null diagnostic is always off
int main() {
    // make a null channel
    pyre::journal::null_t channel("tests.journal.null");

    // if it's active by default
    if (channel) {
        // we have a problem
        throw pyre::journal::firewall_error("active null channel");
    }

    // attempt to activate
    channel.activate();
    // if it's activated
    if (channel) {
        // we have a problem
        throw pyre::journal::firewall_error("null channel was activated");
    }

    // nothing to do
    return 0;
}


// end of file
