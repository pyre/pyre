// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using trash_t = pyre::journal::trash_t;
using firewall_t = pyre::journal::firewall_t;


// a non-fatal firewall hands back the exception it would have raised
int
main()
{
    // make a channel
    firewall_t channel("tests.journal.firewall");
    // send the output to the trash
    channel.device<trash_t>();
    // make sure the firewall isn't fatal
    channel.fatal(false);

    // carefully
    try {
        // raise what the channel hands back
        throw channel << pyre::journal::at() << "nasty bug:" << pyre::journal::newline
                      << "    hello world!" << pyre::journal::endl;
    }
    // if it is the right exception
    catch (const firewall_t::exception_type & error) {
        // verify it carries the page
        assert(error.page().size() == 2);
        assert(error.page()[0] == "nasty bug:");
        assert(error.page()[1] == "    hello world!");
        // and the notes
        assert(error.notes().at("channel") == "tests.journal.firewall");
        assert(error.notes().at("severity") == "firewall");
    }

    // the entry was flushed after it was recorded
    assert(channel.entry().page().empty());

    // all done
    return 0;
}


// end of file
