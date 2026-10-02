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
using myerror_t = pyre::journal::error_t;


// a non-fatal error channel hands back the exception it would have raised
int
main()
{
    // make a channel
    myerror_t channel("tests.journal.error");
    // send the output to the trash
    channel.device<trash_t>();
    // make sure the channel isn't fatal
    channel.fatal(false);

    // carefully
    try {
        // raise what the channel hands back
        throw channel << pyre::journal::at() << "nasty bug:" << pyre::journal::newline
                      << "    hello world!" << pyre::journal::endl;
    }
    // if it is the right exception
    catch (const myerror_t::exception_type & error) {
        // verify it carries the page
        assert(error.page().size() == 2);
        assert(error.page()[0] == "nasty bug:");
        assert(error.page()[1] == "    hello world!");
        // and the notes
        assert(error.notes().at("channel") == "tests.journal.error");
        assert(error.notes().at("severity") == "error");
    }

    // the entry was flushed after it was recorded
    assert(channel.entry().page().empty());

    // all done
    return 0;
}


// end of file
