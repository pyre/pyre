// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type alias
using warning_t = pyre::journal::warning_t;


// exercise the common use case with a fatal channel
int main() {
    // make a warning channel
    warning_t channel("tests.journal.warning");
    // make it fatal
    channel.fatal(true);
    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // we've asked for this to fail, so carefully
    try {
        // inject something into the channel
        channel
            << pyre::journal::at(__HERE__)
            << pyre::journal::note("time", "now")
            << "warning channel:" << pyre::journal::newline
            << "    hello world!" << pyre::journal::endl;
        // unreachable
        throw std::logic_error("unreachable");
    // if all goes well
    } catch (const warning_t::exception_type & error) {
        // make sure the reason was recorded correctly
        assert (error.what() == channel.name() + warning_t::string_type(": warning"));
    }

    // all done
    return 0;
}


// end of file
