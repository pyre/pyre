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
using myerror_t = pyre::journal::error_t;


// basic error example with a non-fatal channel
int main() {
    // make an error channel
    myerror_t channel("tests.journal.error");

    // make it non-fatal
    channel.fatal(false);
    // send the output to the trash
    channel.device<trash_t>();

    // errors are fatal by default, so attempt to
    try {
        // inject something into the channel; no exception should be raised
        channel
            << pyre::journal::at(__HERE__)
            << pyre::journal::note("time", "now")
            << "error channel:" << pyre::journal::newline
            << "    hello world!" << pyre::journal::endl;
    // if the error triggered an exception
    } catch (const myerror_t::exception_type &) {
        // unreachable
        throw std::logic_error("unreachable");
    }

    // all done
    return 0;
}


// end of file
