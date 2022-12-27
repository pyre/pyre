// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using trash_t = pyre::journal::trash_t;
using firewall_t = pyre::journal::firewall_t;


// verify that empty injections in firewall work as expected
int main() {
    // make a firewall
    firewall_t channel("tests.journal.firewall");
    // send the output to the trash
    channel.device<trash_t>();

    // gingerly
    try {
        // inject nothing
        channel << pyre::journal::endl;
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
