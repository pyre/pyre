// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// support
#include "public.h"

// internals
auto
pyre::flow::Product::flush() -> void
{
    // chain up
    Node::flush();
    // go through my readers
    for (auto [slot, reader] : _readers) {
        // and flush them
        reader->flush();
    }
    // all done
    return;
}

auto
pyre::flow::Product::sync() -> void
{
    // go through my writers
    for (auto [slot, writer] : _writers) {
        // and ask each one to refresh me
    }
    // mark me as clean
    clean();
    // all done
    return;
}

// end of file