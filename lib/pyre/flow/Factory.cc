// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// support
#include "public.h"

// invalidate my downstream graph
auto
pyre::flow::Factory::flush() -> void
{
    // chain up
    Node::flush();
    // go through my output slots
    for (auto [name, product] : _outputs) {
        // and invalidate them
        product->flush();
    }
    // all done
    return;
}

// rebuild the product bound to a slot
auto
pyre::flow::Factory::refresh(name_type slot, product_ref_type product) -> void
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.refresh");
    // show me
    channel
        // the factory
        << "factory " << (void *) this
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // the product
        << "is refreshing product " << (void *) product.get()
        << pyre::journal::newline
        // the slot
        << "connected to slot '" << slot << "'"
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);

    // i don't know how to do anything else
    return;
}

// end of file