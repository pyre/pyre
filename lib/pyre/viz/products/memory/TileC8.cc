// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// externals
#include "../external.h"
// forward declarations
#include "../forward.h"
// type aliases
#include "../api.h"

// my class declaration
#include "TileC8.h"

// destructor
pyre::viz::products::memory::TileC8::~TileC8()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.memory.tile_c8");
    // let me know
    channel
        // mark
        << "tile_c8 " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// end of file