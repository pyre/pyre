// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// channel stub
class severity_t : public pyre::journal::channel_t<severity_t> {
    // metamethods
public:
    inline explicit severity_t(const name_type & name) : pyre::journal::channel_t<severity_t>(name)
    {}
};


// exercise the manipulators
int
main()
{
    // make a channel
    severity_t channel("channel");

    // inject something; avoid flushing by using {endl}
    channel
        // locator
        << pyre::journal::at(__HERE__)
        // indentation level
        << pyre::journal::indent(2)
        // detail level
        << pyre::journal::detail(4)
        // metadata
        << pyre::journal::note("time", "now")
        // body
        << "hello world!"
        // flush
        << pyre::journal::newline;

    // verify the indentation level
    assert(channel.dent() == 2);
    // and the detail level
    assert(channel.detail() == 4);

    // get the metadata
    auto meta = channel.entry().notes();
    // verify that our decorations are present
    assert(meta["filename"] == __FILE__);
    assert(meta["line"] == "32");
    assert(meta["function"] == __func__);
    assert(meta["time"] == "now");

    // all done
    return 0;
}


// end of file
