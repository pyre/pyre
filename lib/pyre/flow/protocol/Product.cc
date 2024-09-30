// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// support
#include "../public.h"

// destructor
pyre::flow::protocol::Product::~Product()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.products.destroy");
    // show me
    channel
        // the product
        << "product " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);
    // all done
    return;
}

// bindings
auto
pyre::flow::protocol::Product::addReader(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // add the factory to my pile of readers
    _readers.insert({ slot, factory });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocol::Product::addWriter(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // add the factory to my pile of writers
    _writers.insert({ slot, factory });
    // invalidate me
    flush();
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocol::Product::removeReader(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // remove the factory from my pile of readers
    _readers.extract({ slot, factory });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocol::Product::removeWriter(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // remove the factory from my pile of writers
    _writers.extract({ slot, factory });
    // return a reference to me
    return ref();
};

// internals
auto
pyre::flow::protocol::Product::flush() -> void
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.products.flush");
    // show me
    channel
        // the product
        << "product '" << name() << "' at " << this << ": flush"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);
    // chain up
    Node::flush();
    // mark me
    dirty();
    // go through my readers
    for (auto & [slot, reader] : _readers) {
        // and flush each one
        reader->flush();
    }
    // all done
    return;
}

auto
pyre::flow::protocol::Product::make() -> product_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.products.make");
    // show me
    channel
        // sign on
        << "product '" << name() << "' at " << this << ": make"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // make a reference
    auto self = ref();
    // if i'm stale
    if (_stale) {
        // go through my writers
        for (auto & [slot, writer] : _writers) {
            // ask each one to refresh me
            writer->make(slot, self);
        }
        // mark me as clean
        clean();
    }
    // all done
    return self;
}

// end of file