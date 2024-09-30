// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using trash_t = pyre::journal::trash_t;
using firewall_t = pyre::journal::firewall_t;


// exercise the channel manipulators
int
main()
{
    // make an firewall channel
    firewall_t channel("tests.journal.firewall");

    // send the message to the trash
    channel.device<trash_t>();

    // set the level of decoration
    pyre::journal::chronicler_t::decor(3);

    // carefully
    try {
        // inject something into the channel
        channel
#if defined(__cpp_lib_source_location)
            //  location
            << pyre::journal::here()
#else
            << pyre::journal::at(__HERE__)
#endif
            // some metadata
            << pyre::journal::note("time", "now")
            // sign on
            << "firewall channel:"
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // a message
            << "hello world!"
            << pyre::journal::newline
            // outdent
            << pyre::journal::outdent
            // flush
            << pyre::journal::endl;
        // firewalls are fatal by default, so we shouldn't be able to get here
        throw std::logic_error("unreachable");
        // if all goes well
    } catch (const firewall_t::exception_type & firewall) {
        // make sure the reason was recorded correctly
        assert(firewall.what() == channel.name() + firewall_t::string_type(": FIREWALL BREACHED!"));
    }


    // all done
    return 0;
}


// end of file
