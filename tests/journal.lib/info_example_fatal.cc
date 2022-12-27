// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type alias
using info_t = pyre::journal::info_t;


// exercise a fatal channel
int main() {
    // make an info channel
    info_t channel("tests.journal.info");
    // make it fatal
    channel.fatal(true);
    // send the message to the trash
    channel.device<pyre::journal::trash_t>();

    // we've asked for this to fail, so carefully
    try {
        // inject something into the channel
        channel
            << pyre::journal::at(__HERE__)
            << pyre::journal::note("time", "now")
            << "info channel:" << pyre::journal::newline
            << "    hello world!" << pyre::journal::endl;
        // unreachable
        throw std::logic_error("unreachable");
        // if all goes well
    } catch (const info_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert (error.what() == channel.name() + info_t::string_type(": info"));
    }

    // all done
    return 0;
}


// end of file
