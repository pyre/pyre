// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include "../public.h"

// destructor
pyre::flow::protocols::Product::~Product()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.products.destroy");
    // show me
    channel
        // where
        << pyre::journal::at()
        // the product
        << "product " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;
    // all done
    return;
}

// bindings
auto
pyre::flow::protocols::Product::addReader(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // add the factory to my pile of readers
    _readers.insert({ slot, factory });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocols::Product::addWriter(name_type slot, factory_ref_type factory)
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
pyre::flow::protocols::Product::removeReader(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // remove the factory from my pile of readers
    _readers.erase({ slot, factory });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocols::Product::removeWriter(name_type slot, factory_ref_type factory)
    -> product_ref_type
{
    // remove the factory from my pile of writers
    _writers.erase({ slot, factory });
    // return a reference to me
    return ref();
};

// internals
auto
pyre::flow::protocols::Product::flush() -> void
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.products.flush");
    // show me
    channel
        // where
        << pyre::journal::at()
        // the product
        << "product '" << name() << "' at " << this << ": flush"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;
    // if i am stale already, so is everything downstream of me
    if (_stale) {
        // so there is nothing to do
        return;
    }
    // chain up
    Node::flush();
    // mark me
    dirty();
    // forget the readers that have gone away
    std::erase_if(_readers, [](const slot_type & binding) {
        // which the expired references are
        return std::get<1>(binding).expired();
    });
    // go through the rest
    for (auto & [slot, reader] : _readers) {
        // and flush each one, if it is still around
        if (auto factory = reader.lock()) {
            // by asking it to flush
            factory->flush();
        }
    }
    // all done
    return;
}

auto
pyre::flow::protocols::Product::make() -> product_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.products.make");
    // show me
    channel
        // where
        << pyre::journal::at()
        // sign on
        << "product '" << name() << "' at " << this << ": make"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;

    // make a reference
    auto self = ref();
    // if i'm stale
    if (_stale) {
        // forget the writers that have gone away
        std::erase_if(_writers, [](const slot_type & binding) {
            // which the expired references are
            return std::get<1>(binding).expired();
        });
        // go through the rest
        for (auto & [slot, writer] : _writers) {
            // get the factory
            auto factory = writer.lock();
            // the inputs it cannot read
            auto lost = factory->missing();
            // if there are any
            if (!lost.empty()) {
                // make a channel
                auto channel = pyre::journal::error_t("pyre.flow.products.make");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "cannot make '" << name() << "'"
                    << pyre::journal::newline
                    // why
                    << "factory '" << factory->name() << "' cannot read its input slots"
                    << pyre::journal::newline << pyre::journal::indent;
                // go through the slots
                for (const auto & input : lost) {
                    // name each one
                    channel << input << pyre::journal::newline;
                }
                // flush
                channel << pyre::journal::outdent << pyre::journal::endl;
                // and leave me stale
                return self;
            }
            // ask it to refresh me
            factory->make(slot, self);
        }
        // mark me as clean
        clean();
    }
    // all done
    return self;
}


// end of file
