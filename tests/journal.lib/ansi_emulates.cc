// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using ansi_t = pyre::journal::ansi_t;


// verify that we can detect ANSI emulation reliably; the harness sets things up and passes a
// flag on the command line so we can set our expectations
int main(int argc, char *argv[]) {

    // the test harness hands its expectation
    bool expectation = argc > 1 ? std::atoi(argv[1]) : true;
    // ask the wrapper whether the underlying terminal type is ANSI compatible
    auto observation = ansi_t::compatible();

    // verify that expectation and observation match
    assert (expectation == observation);

    // all done
    return 0;
}


// end of file
