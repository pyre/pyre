// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// support
#include "../public.h"

// destructor
pyre::flow::protocol::Factory::~Factory()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.destroy");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);
    // all done
    return;
}

// bindings
auto
pyre::flow::protocol::Factory::addInput(const name_type & slot, product_ref_type product) -> factory_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.input");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": adding an input"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // the slot
        << "slot: " << slot
        << pyre::journal::newline
        // the product
        << "product: '" << product->name() << "' at " << product.get()
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);
    // notify the product i am one of its readers
    product->addReader(slot, ref());
    // add the binding to my pile
    _inputs.insert({ slot, product });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocol::Factory::addOutput(const name_type & slot, product_ref_type product) -> factory_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.output");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": adding an output"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // the slot
        << "slot: " << slot
        << pyre::journal::newline
        // the product
        << "product: " << product.get()
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);
    // notify the product i am one of its writers
    product->addWriter(slot, ref());
    // add the binding to my pile
    _outputs.insert({ slot, product });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocol::Factory::removeInput(const name_type & slot) -> factory_ref_type
{
    // make a handle to me
    auto self = ref();
    // find the product
    auto product = input(slot);
    // detach me as a product readers
    product->removeReader(slot, self);
    // remove the binding from my pile
    _inputs.extract(slot);

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.input");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": removing an input"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // the slot
        << "slot: " << slot
        << pyre::journal::newline
        // the product
        << "product: " << product.get()
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);

    // return a reference to me
    return self;
};

auto
pyre::flow::protocol::Factory::removeOutput(const name_type & slot) -> factory_ref_type
{
    // make a handle to me
    auto self = ref();
    // find the product
    auto product = output(slot);
    // detach me as a product writer
    product->removeWriter(slot, self);
    // remove the binding from my pile
    _outputs.extract(slot);

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.output");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": removing an output"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // the slot
        << "slot: " << slot
        << pyre::journal::newline
        // the product
        << "product: " << product.get()
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);

    // return a reference to me
    return self;
};

// invalidate my downstream graph
auto
pyre::flow::protocol::Factory::flush() -> void
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.flush");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": flush"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);
    // chain up
    Node::flush();
    // go through my output slots
    for (auto & [name, product] : _outputs) {
        // and invalidate them
        product->flush();
    }
    // all done
    return;
}

// rebuild the product bound to a slot
auto
pyre::flow::protocol::Factory::make(const name_type & slot, product_ref_type product) -> factory_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.make");
    // show me
    channel
        // the factory
        << "factory '" << name() << "' at " << this << ": make"
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // the product
        << "product: '" << product->name() << "' at " << product.get()
        << pyre::journal::newline
        // the slot
        << "slot: '" << slot << "'"
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);

    // go through my inputs
    for (auto & [slot, product] : _inputs) {
        // find the stale ones
        if (product->stale()) {
            // show me
            channel
                // the factory
                << "factory '" << name() << "' at " << this << ": make"
                << pyre::journal::newline
                // indent
                << pyre::journal::indent
                // the product
                << "making product: '" << product->name() << "' at " << product.get()
                << pyre::journal::newline
                // outdent
                << pyre::journal::outdent
                // flush
                << pyre::journal::endl(__HERE__);
            // and refresh them
            product->make();
            // show me
            channel
                // the factory
                << "factory '" << name() << "' at " << this << ": make"
                << pyre::journal::newline
                // indent
                << pyre::journal::indent
                // the product
                << "done making product: '" << product->name() << "' at " << product.get()
                << pyre::journal::newline
                // outdent
                << pyre::journal::outdent
                // flush
                << pyre::journal::endl(__HERE__);
        }
    }

    // i don't know how to do anything else
    return ref();
}

// end of file