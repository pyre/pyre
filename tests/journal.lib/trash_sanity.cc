// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias the type
using trash_t = pyre::journal::trash_t;


// verify we can instantiate the trash can
int main() {
    // instantiate
    trash_t trash;
    // check its name
    assert (trash.name() == "trash");

    // all done
    return 0;
}


// end of file
