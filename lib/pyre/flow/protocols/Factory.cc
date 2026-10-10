// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include "../public.h"

// destructor
pyre::flow::protocols::Factory::~Factory()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.destroy");
    // show me
    channel
        // where
        << pyre::journal::at()
        // the factory
        << "factory '" << name() << "' at " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;
    // all done
    return;
}

// bindings
auto
pyre::flow::protocols::Factory::addInput(const name_type & slot, product_ref_type product)
    -> factory_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.input");
    // show me
    channel
        // where
        << pyre::journal::at()
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
        << pyre::journal::endl;
    // notify the product i am one of its readers
    product->addReader(slot, ref());
    // add the binding to my pile
    _inputs.insert({ slot, product });
    // what i compute depends on my inputs, so everything downstream of me is stale
    flush();
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocols::Factory::addOutput(const name_type & slot, product_ref_type product)
    -> factory_ref_type
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.output");
    // show me
    channel
        // where
        << pyre::journal::at()
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
        << pyre::journal::endl;
    // notify the product i am one of its writers
    product->addWriter(slot, ref());
    // add the binding to my pile
    _outputs.insert({ slot, product });
    // return a reference to me
    return ref();
};

auto
pyre::flow::protocols::Factory::removeInput(const name_type & slot) -> factory_ref_type
{
    // make a handle to me
    auto self = ref();
    // find the product
    auto product = input(slot);
    // if it is still around
    if (product) {
        // detach me as one of its readers
        product->removeReader(slot, self);
    }
    // remove the binding from my pile
    _inputs.erase(slot);

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.input");
    // show me
    channel
        // where
        << pyre::journal::at()
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
        << pyre::journal::endl;

    // return a reference to me
    return self;
};

auto
pyre::flow::protocols::Factory::removeOutput(const name_type & slot) -> factory_ref_type
{
    // make a handle to me
    auto self = ref();
    // find the product
    auto product = output(slot);
    // detach me as a product writer
    product->removeWriter(slot, self);
    // remove the binding from my pile
    _outputs.erase(slot);

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.output");
    // show me
    channel
        // where
        << pyre::journal::at()
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
        << pyre::journal::endl;

    // return a reference to me
    return self;
};

// invalidate my downstream graph
auto
pyre::flow::protocols::Factory::flush() -> void
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.flush");
    // show me
    channel
        // where
        << pyre::journal::at()
        // the factory
        << "factory '" << name() << "' at " << this << ": flush"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;
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
pyre::flow::protocols::Factory::make(const name_type & slot, product_ref_type product)
    -> factory_ref_type
{
    // if i know the family of the component i stand for
    if (!_family.empty()) {
        // report my work on its channel, so whoever watches it can tell i ran
        auto report = pyre::journal::debug_t(_family);
        // say what i am making
        report
            // where
            << pyre::journal::at()
            // what
            << "'" << name() << "' makes '" << product->name() << "' through its slot '" << slot
            << "'"
            // flush
            << pyre::journal::endl;
    }
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow.factories.make");
    // show me
    channel
        // where
        << pyre::journal::at()
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
        << pyre::journal::endl;

    // go through my inputs
    for (auto & [slot, input] : _inputs) {
        // get the product, if it is still around
        auto product = input.lock();
        // find the stale ones
        if (product && product->stale()) {
            // show me
            channel
                // where
                << pyre::journal::at()
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
                << pyre::journal::endl;
            // and refresh them
            product->make();
            // show me
            channel
                // where
                << pyre::journal::at()
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
                << pyre::journal::endl;
        }
    }

    // i don't know how to do anything else
    return ref();
}


// the descriptions of my slots
auto
pyre::flow::protocols::Factory::slots() const -> const slots_type &
{
    // a factory that does not describe its slots has none
    static const slots_type none {};
    // hand them off
    return none;
}


// the descriptions of my settings
auto
pyre::flow::protocols::Factory::settings() const -> const settings_type &
{
    // a factory that does not describe its settings has none
    static const settings_type none {};
    // hand them off
    return none;
}


// the description of my slot {name}
auto
pyre::flow::protocols::Factory::slot(const name_type & name) const -> const slot_type *
{
    // get my slots
    const auto & table = slots();
    // look for the one with this name
    auto found = std::find_if(table.begin(), table.end(), [&name](const slot_type & slot) {
        // by comparing names
        return slot.name() == name;
    });
    // hand off its address, or nothing if it is not there
    return found == table.end() ? nullptr : &*found;
}


// bind my slot {name} to {product}
auto
pyre::flow::protocols::Factory::bind(const name_type & name, product_ref_type product) -> bool
{
    // look up the slot
    auto description = slot(name);
    // a slot i do not have, or a product it does not take
    if (description == nullptr || !description->accepts(product)) {
        // binds nothing
        return false;
    }
    // forget whatever the slot is bound to
    unbind(name);
    // an input
    if (description->reads()) {
        // is bound, which makes everything downstream of me stale
        addInput(name, product);
        // all done
        return true;
    }
    // an output is bound, which makes it and everything downstream of it stale
    addOutput(name, product);
    // all done
    return true;
}


// undo the binding of my slot {name}
auto
pyre::flow::protocols::Factory::unbind(const name_type & name) -> bool
{
    // look up the slot
    auto description = slot(name);
    // a slot i do not have
    if (description == nullptr) {
        // has nothing to undo
        return false;
    }
    // an input
    if (description->reads()) {
        // that is not bound
        if (_inputs.count(name) == 0) {
            // has nothing to undo
            return false;
        }
        // otherwise, undo its binding
        removeInput(name);
        // all done
        return true;
    }
    // an output that is not bound
    if (_outputs.count(name) == 0) {
        // has nothing to undo
        return false;
    }
    // otherwise, undo its binding
    removeOutput(name);
    // all done
    return true;
}


// read my setting {name}
auto
pyre::flow::protocols::Factory::get(const name_type & name) const
    -> std::optional<setting_value_type>
{
    // go through my settings
    for (const auto & setting : settings()) {
        // until the one with this name
        if (setting.name() == name) {
            // read it
            return setting.get(*this);
        }
    }
    // a setting i do not have has no value
    return std::nullopt;
}


// change my setting {name}
auto
pyre::flow::protocols::Factory::set(const name_type & name, const setting_value_type & value)
    -> bool
{
    // go through my settings
    for (const auto & setting : settings()) {
        // until the one with this name
        if (setting.name() == name) {
            // change it
            return setting.set(*this, value);
        }
    }
    // a setting i do not have cannot be changed
    return false;
}


// the input slots i cannot read
auto
pyre::flow::protocols::Factory::missing() const -> std::vector<name_type>
{
    // the slots
    auto lost = std::vector<name_type>();
    // go through the descriptions of my slots
    for (const auto & description : slots()) {
        // an input that is not bound
        if (description.reads() && _inputs.count(description.name()) == 0) {
            // cannot be read
            lost.push_back(description.name());
        }
    }
    // go through my bound inputs
    for (const auto & [slot, input] : _inputs) {
        // one whose product has gone away
        if (input.expired()) {
            // cannot be read either
            lost.push_back(slot);
        }
    }
    // hand them off
    return lost;
}


// end of file
