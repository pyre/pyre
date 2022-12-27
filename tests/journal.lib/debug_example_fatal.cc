// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type alias
using debug_t = pyre::journal::debug_t;


// exercise the channel manipulators
int main() {
    // make a debug channel
    debug_t channel("tests.journal.debug");
    // activate it
    channel.activate();
    // make it fatal
    channel.fatal(true);
    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // we've asked for this to fail, so carefully
    try {
        // inject something into the channel
        channel
            // location
            << pyre::journal::at(__HERE__)
            // some metadata
            << pyre::journal::note("time", "now")
            // a message with a newline
            << "debug channel:" << pyre::journal::newline
            // another message and a flush
            << "    hello world!" << pyre::journal::endl;
        // unreachable
        throw std::logic_error("unreachable");
    // if all goes well
    } catch (const debug_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert (error.what() == channel.name() + debug_t::string_type(": debug"));
    }

    // all done
    return 0;
}


// end of file
