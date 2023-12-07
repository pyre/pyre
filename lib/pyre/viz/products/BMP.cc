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
#include "BMP.h"

// destructor
pyre::viz::products::BMP::~BMP()
{
    // free my buffer
    delete[] _data;

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.bmp");
    // let me know
    channel
        // mark
        << "bmp: destroying bitmap at "
        << (void *) this
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// internals
auto
pyre::viz::products::BMP::flush() -> void
{
    // chain up
    pyre::flow::product_t::flush();
    // invalidate my memory buffer
    delete[] _data;

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.bmp");
    // let me know
    channel
        // mark
        << "bmp: flushing bitmap at "
        << (void *) this
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// end of file