// -*- c++ -*-
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


// verify that detaching a device removes every one of its attachments, and only those
int
main()
{
    // make a few devices
    auto first = std::make_shared<trash_t>();
    auto second = std::make_shared<trash_t>();
    auto stranger = std::make_shared<trash_t>();
    // make a splitter that holds the first one twice
    splitter_t splitter;
    // attach them
    splitter.attach(first).attach(second).attach(first);
    // detach the first one
    splitter.detach(first);
    // only the second one is left
    assert(splitter.outputs().size() == 1);
    assert(splitter.outputs()[0] == second);
    // detaching a device that is not attached changes nothing
    splitter.detach(stranger);
    // so the second one is still there
    assert(splitter.outputs().size() == 1);
    // all done
    return 0;
}


// end of file
