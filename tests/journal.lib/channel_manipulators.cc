// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <source_location>


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
        << pyre::journal::at()
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

    // the compiler's view of where we are, in the same function as the locator
    const auto here = std::source_location::current();
    // get the metadata
    auto meta = channel.entry().notes();
    // verify that our decorations are present
    assert(meta["filename"] == here.file_name());
    assert(meta["line"] == "34");
    assert(meta["function"] == here.function_name());
    assert(meta["time"] == "now");

    // all done
    return 0;
}


// end of file
