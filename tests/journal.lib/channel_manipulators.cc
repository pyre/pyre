// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// channel stub
class severity_t : public pyre::journal::channel_t<severity_t> {
    // metamethods
public:
    inline explicit severity_t(const name_type & name) :
        pyre::journal::channel_t<severity_t>(name) {}
};


// exercise the manipulators
int main() {
    // make a channel
    severity_t channel("channel");

    // inject something; avoid flushing by using {endl}
    channel
        << pyre::journal::at(__HERE__)
        << pyre::journal::detail(4)
        << pyre::journal::note("time", "now")
        << "hello world!" << pyre::journal::newline;

    // verify the detail level
    assert (channel.detail() == 4);

    // get the metadata
    auto meta = channel.entry().notes();
    // verify that our decorations are present
    assert (meta["filename"] == __FILE__);
    assert (meta["line"] == "29");
    assert (meta["function"] == __func__);
    assert (meta["time"] == "now");

    // all done
    return 0;
}


// end of file
