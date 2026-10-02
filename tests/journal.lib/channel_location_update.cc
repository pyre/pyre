// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <source_location>
#include <string>


// a later entry of the same channel reports its own location, not that of the first one
int
main()
{
    // make a channel
    pyre::journal::info_t channel("tests.journal.location");
    // send its output to the trash
    channel.device<pyre::journal::trash_t>();

    // record an entry
    channel << pyre::journal::at() << "first" << pyre::journal::endl;
    // mark a different place
    const auto where = std::source_location::current();
    // and record another entry there
    channel << pyre::journal::at(where) << "second" << pyre::journal::endl;

    // the notes hold the location of the second entry
    return channel.entry().notes().at("line") == std::to_string(where.line()) ? 0 : 1;
}


// end of file
