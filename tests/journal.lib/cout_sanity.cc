// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias the type
using console_t = pyre::journal::cout_t;


// instantiate the {cout} console and make sure its name is correct
int main() {
    // instantiate
    console_t console;
    // check its name
    assert (console.name() == "cout");

    // all done
    return 0;
}


// end of file
