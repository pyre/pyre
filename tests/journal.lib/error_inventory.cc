// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>

// support
#include <cassert>


// verify that we can manipulate the error inventory state
int main() {
    // make a default inventory
    pyre::journal::error_t error("error");

    // by default, its device is null
    assert(error.device() == pyre::journal::chronicler_t::device());

    // verify it is on
    assert(error.active() == true);
    // flip it
    error.active(false);
    // check again
    assert(error.active() == false);

    // verify it's fatal by default
    assert(error.fatal() == true);
    // flip it
    error.fatal(false);
    // check again
    assert(error.fatal() == false);

    // all done
    return 0;
}


// end of file
