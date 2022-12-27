// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using myerror_t = pyre::journal::error_t;
using trash_t = pyre::journal::trash_t;


// verify that repeated injections work correctly
int main() {
    // make an error channel
    myerror_t channel("tests.journal.error");

    // send the output to the trash
    channel.device<trash_t>();

    // inject repeatedly
    for (auto i=0; i<10; ++i) {
        // carefully
        try {
            // inject something
            channel << "i: " << i << pyre::journal::endl;
            // errors are fatal by default, so we shouldn't be able to get here
            throw std::logic_error("unreachable");
            // if all goes well
        }  catch (const myerror_t::exception_type & error) {
            // make sure the reason was recorded correctly
            assert (error.what() == channel.name() + myerror_t::string_type(": application error"));
        }
    }

    // all done
    return 0;
}


// end of file
