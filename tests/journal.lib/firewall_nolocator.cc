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


// verify that injection without location information works correctly
int main() {
    // make a firewall
    firewall_t channel("tests.journal.firewall");

    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // gingerly
    try {
        // inject nothing
        channel << "a firewall without location information" << pyre::journal::endl;
        // shouldn't be able to get here
        throw std::logic_error("unreachable");
    // if all goes well
    } catch (const firewall_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert (error.what() == channel.name() + firewall_t::string_type(": FIREWALL BREACHED!"));
    }

    // all done
    return 0;
}


// end of file
