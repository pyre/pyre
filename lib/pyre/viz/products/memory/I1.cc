// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// externals
#include "../../public.h"
// forward declarations
#include "../../forward.h"
// type aliases
#include "../../api.h"

// my class declaration
#include "I1.h"

// destructor
pyre::viz::products::memory::I1::~I1()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.memory.i1");
    // let me know
    channel
        // mark
        << "i1: destroying cell at "
        << this
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}
