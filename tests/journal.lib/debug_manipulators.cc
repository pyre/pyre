// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise the channel manipulators
int main() {
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // try injecting something into the channel; careful not to flush
    channel
        << pyre::journal::at(__HERE__)
        << pyre::journal::note("time", "now")
        << "debug channel:" << pyre::journal::newline
        << "    hello world!" << pyre::journal::newline;

    // get the current channel page
    auto page = channel.entry().page();
    // verify
    assert (page[0] == "debug channel:");
    assert (page[1] == "    hello world!");

    // get the metadata
    auto metadata = channel.entry().notes();
    // verify
    assert (metadata["filename"] == __FILE__);
    assert (metadata["line"] == "20");
    assert (metadata["time"] == "now");

    // all done
    return 0;
}


// end of file
