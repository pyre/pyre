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


// exercise the channel manipulators
int
main()
{
    // make a firewall
    firewall_t channel("tests.journal.firewall");

    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // firewalls are fatal by default, so attempt
    try {
        // inject something into the channel
        channel
            // location
            << pyre::journal::at(__HERE__)
            // some metadata
            << pyre::journal::note("time", "now")
            // a structured message
            << "top level"
            << pyre::journal::newline
            // level one
            << pyre::journal::indent << "level 1"
            << pyre::journal::newline
            // level 2
            << pyre::journal::indent(2) << "level 3"
            << pyre::journal::newline
            // level 2
            << pyre::journal::outdent << "back to level 2"
            << pyre::journal::newline
            // level 1
            << pyre::journal::outdent(2) << "back to top level"
            << pyre::journal::newline
            // flush
            << pyre::journal::endl;
        // unreachable
        throw std::logic_error("unreachable");
        // if all goes well
    } catch (const firewall_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert(error.what() == channel.name() + firewall_t::string_type(": FIREWALL BREACHED!"));
    }

    // all done
    return 0;
}


// end of file
