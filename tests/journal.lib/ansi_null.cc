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


// verify that the null color table supports all possible requests
int main() {
    // ask for a color that's unlikely to be there
    auto strange = ansi_t::null("a-very-unlikely-color-name");
    // verify that the color sequences it returns are empty strings
    assert (strange.empty());
    // all done
    return 0;
}


// end of file
