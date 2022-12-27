// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias the type
using console_t = pyre::journal::cerr_t;


// exercise the {cerr} console
int main() {
    // instantiate
    console_t console;
    // check its name
    assert (console.name() == "cerr");

    // all done
    return 0;
}


// end of file
