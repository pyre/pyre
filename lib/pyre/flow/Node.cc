// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// externals
#include "external.h"
// forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// my class declaration
#include "Node.h"

// internals
auto
pyre::flow::Node::flush() -> void
{
    // mark me as stale
    _stale = true;
    // all done
    return;
}

// end of file