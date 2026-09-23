// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>

// type aliases
using splitter_t = pyre::journal::splitter_t;
using trash_t = pyre::journal::trash_t;


// verify that a splitter can be made and devices attached to it
int
main()
{
    // make a splitter
    splitter_t splitter;
    // check its name
    assert(splitter.name() == "splitter");
    // it starts out with no devices
    assert(splitter.outputs().empty());
    // attach a couple
    splitter.attach(std::make_shared<trash_t>()).attach(std::make_shared<trash_t>());
    // and they are there, in order
    assert(splitter.outputs().size() == 2);
    // all done
    return 0;
}


// end of file
