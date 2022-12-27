// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using firewall_t = pyre::journal::firewall_t;


// verify the basic channel state
int main() {
    // make a firewall
    firewall_t channel("tests.journal.firewall");

    // check its name
    assert (channel.name() == "tests.journal.firewall");
    // by default, it should be active
    assert (channel);
    // and fatal
    assert (channel.fatal());

    // all done
    return 0;
}


// end of file
