// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using trash_t = pyre::journal::trash_t;
using channel_t = pyre::journal::debug_t;


// verify that channels that have the same name share the same state
int main() {
    // make a channel
    channel_t ch_1("tests.journal");
    // flip all state away from the defaults
    ch_1.active(true);
    ch_1.fatal(true);
    // install a trash can as the channel device
    ch_1.device<trash_t>();

    // make another with the same name
    channel_t ch_2("tests.journal");
    // verify that it sees the common state
    assert(ch_2.active() == ch_1.active());
    assert(ch_2.fatal() == ch_1.fatal());
    assert(ch_2.device() == ch_1.device());

    // all done
    return 0;
}


// end of file
