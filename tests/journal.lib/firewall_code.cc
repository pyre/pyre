// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise decorating a message with a code
int
main()
{
    // make a channel
    pyre::journal::firewall_t channel("tests.journal.firewall");

    // set the chronicler maximum detail level so the code is rendered
    pyre::journal::chronicler_t::decor(2);
    // activate it
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // carefully
    try {
        // inject something into the channel
        channel
            // add the code
            << pyre::journal::code(10)
            // say something
            << "hello world!"
            // and flush
            << pyre::journal::endl(__HERE__);
        // firewalls are fatal by default, so we shouldn't be able to get here
        throw std::logic_error("unreachable");
        // if all goes well
    } catch (const pyre::journal::firewall_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert(error.what() == channel.name() + pyre::journal::string_t(": FIREWALL BREACHED!"));
    }

    // all done
    return 0;
}


// end of file
