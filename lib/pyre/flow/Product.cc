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

// super class
#include "Node.h"
// my class declaration
#include "Product.h"

// internals
auto
pyre::flow::Product::flush() -> void
{
    // chain up
    Node::flush();
    // all done
    return;
}

// end of file