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


// exercise a non-fatal channel
int main() {
    // make a firewall
    firewall_t channel("tests.journal.firewall");

    // send the output to the trash
    channel.device<trash_t>();
    // make sure the firewall isn't fatal
    channel.fatal(false);

    // firewalls are fatal by default, so attempt to
    try {
        // inject something into the channel
        channel
            << pyre::journal::at(__HERE__)
            << pyre::journal::note("time", "now")
            << "nasty bug:" << pyre::journal::newline
            << "    hello world!" << pyre::journal::endl;
    // if the firewall triggered the exception
    } catch (const firewall_t::exception_type &) {
        // unreachable
        throw std::logic_error("unreachable");
    }

    // all done
    return 0;
}


// end of file
