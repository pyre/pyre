// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>


// a note set again on a later entry of the same channel takes the new value
int
main()
{
    // make a channel
    pyre::journal::info_t channel("tests.journal.notes");
    // send its output to the trash
    channel.device<pyre::journal::trash_t>();

    // record an entry with a note
    channel << pyre::journal::note("time", "then") << "first" << pyre::journal::endl;
    // record another with a new value for the same note
    channel << pyre::journal::note("time", "now") << "second" << pyre::journal::endl;

    // the notes outlive the entry, and hold the latest value
    return channel.entry().notes().at("time") == "now" ? 0 : 1;
}


// end of file
