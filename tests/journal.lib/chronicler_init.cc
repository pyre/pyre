// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

#include <iostream>
// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using debug_t = pyre::journal::debug_t;
using chronicler_t = pyre::journal::chronicler_t;


// hand the command line arguments to the {chronicler} initializer
int main(int argc, char* argv[]) {
    // register the command line with the {chronicler}
    chronicler_t::init(argc, argv);

    // we expect the detail level to be 5
    assert (chronicler_t::detail() == 5);

    // and the following channels to be active
    assert (debug_t("test.init.one"));
    assert (debug_t("test.init.two"));

    // all done
    return 0;
}


// end of file
