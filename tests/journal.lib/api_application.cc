// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that the initial chronicler global state is as expected
int main() {
    // make a name
    pyre::journal::value_t app("api");
    // register the name
    pyre::journal::application(app);

    // get the chronicler notes
    auto & notes = pyre::journal::chronicler_t::notes();
    // verify that the key is present and has the right value
    assert (notes.at("application") == app);

    // all done
    return 0;
}


// end of file
