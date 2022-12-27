// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>

// support
#include <cassert>


// convenience
using inventory_t = pyre::journal::firewall_t::inventory_type;

// verify that we can manipulate the firewall inventory state
int main() {
    // make a channel
    pyre::journal::firewall_t firewall("error");

    // by default, its device is whatever the global default is
    assert(firewall.device() == pyre::journal::chronicler_t::device());

    // verify it is on
    assert(firewall.active() == true);
    // flip it
    firewall.active(false);
    // check again
    assert(firewall.active() == false);

    // verify it's fatal by default
    assert(firewall.fatal() == true);
    // flip it
    firewall.fatal(false);
    // check again
    assert(firewall.fatal() == false);

    // all done
    return 0;
}


// end of file
