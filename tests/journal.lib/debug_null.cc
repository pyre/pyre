// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// disable the debug channels
#define NDEBUG 1
#undef PYRE_CORE
// get the journal
#include <pyre/journal.h>

// re-enable debugging support so we have assert
#undef NDEBUG
// support
#include <cassert>


// verify that when NDEBUG is on, {debug_t} becomes {null_t}
int main() {
    // verify that {debug_t} is a {null_t}
    static_assert ((std::is_same<pyre::journal::debug_t, pyre::journal::null_t>::value));

    // make a channel
    pyre::journal::debug_t channel("tests.journal.debug");
    // activate it
    channel.activate();

    // inject something
    channel
        // location
        << pyre::journal::at(__HERE__)
        // some metadata
        << pyre::journal::note("time", "now")
        // a message with a newline
        << "debug channel:" << pyre::journal::newline
        // another message and a flush
        << "    hello world!" << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
