// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that flushing the channel resets its buffers correctly
int main() {
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");
    // activate it
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // try injecting something into the channel
    channel
        << pyre::journal::at(__HERE__)
        << pyre::journal::note("time", "now")
        << "    hello world!" << pyre::journal::endl;

    // verify that the buffer is empty
    assert (channel.entry().buffer().str().empty());
    // the page is empty
    assert (channel.entry().page().empty());
    // but the metadata has been retained
    assert (!channel.entry().notes().empty());

    // all done
    return 0;
}


// end of file
