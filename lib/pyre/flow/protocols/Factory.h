// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "Node.h"
#include "Slot.h"
#include "Setting.h"

class pyre::flow::protocols::Factory : public Node {
    // type aliases
public:
    // me
    using self_type = Factory;
    // my superclass
    using super_type = Node;
    // my inputs, by slot, which i do not keep alive
    using inputs_type = std::map<name_type, product_weakref_type>;
    // my outputs, by slot, which i own
    using outputs_type = std::map<name_type, product_ref_type>;
    // the descriptions of my slots
    using slot_type = Slot;
    using slots_type = std::vector<slot_type>;
    // the descriptions of my settings, and their values
    using setting_type = Setting;
    using settings_type = std::vector<setting_type>;
    using setting_value_type = setting_type::value_type;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Factory();
    // constructor; not usable directly. call {create} instead
    inline Factory(sentinel_type, const name_type &);

    // accessors
public:
    // look up the product bound to an input {slot}; nothing if it is not bound, or the product
    // has gone away
    inline auto input(const name_type & slot) const -> product_ref_type;
    // look up the product bound to an output {slot}
    inline auto output(const name_type & slot) const -> product_ref_type;

    // access to the full set of bindings
    inline auto inputs() const -> const inputs_type &;
    inline auto outputs() const -> const outputs_type &;

    // introspection
public:
    // the descriptions of my slots; a factory that does not describe them has none, and binds
    // nothing through {bind}
    virtual auto slots() const -> const slots_type &;
    // the descriptions of my settings; none, unless a factory describes them
    virtual auto settings() const -> const settings_type &;
    // the description of my slot {name}, or nothing if i have no such slot
    auto slot(const name_type & name) const -> const slot_type *;

    // bindings and settings by name, checked against my descriptions
public:
    // bind my slot {name} to {product}, replacing whatever was bound to it; false, and nothing
    // bound, if i have no such slot or {product} is not one it takes
    auto bind(const name_type & name, product_ref_type product) -> bool;
    // undo the binding of my slot {name}; false if i have no such slot or it is not bound
    auto unbind(const name_type & name) -> bool;
    // read my setting {name}; nothing if i have no such setting
    auto get(const name_type & name) const -> std::optional<setting_value_type>;
    // change my setting {name}; false if i have no such setting or {value} is not of its type
    auto set(const name_type & name, const setting_value_type & value) -> bool;

    // flow protocol
public:
    // bindings; binding an input flushes me, since what i compute depends on my inputs, and
    // binding an output flushes the product, since its contents are not mine yet; undoing a
    // binding flushes nothing, since what i computed stays valid until a replacement is bound
    virtual auto addInput(const name_type & slot, product_ref_type product) -> factory_ref_type;
    virtual auto addOutput(const name_type & slot, product_ref_type product) -> factory_ref_type;

    virtual auto removeInput(const name_type & slot) -> factory_ref_type;
    virtual auto removeOutput(const name_type & slot) -> factory_ref_type;

    // build a reference to me
    inline auto ref() -> factory_ref_type;
    // invalidate me
    virtual auto flush() -> void override;
    // rebuild the product connected to one of my slots
    virtual auto make(const name_type & slot, product_ref_type product) -> factory_ref_type;

    // implementation details - data
private:
    // my inputs, which i do not keep alive
    inputs_type _inputs;
    // my outputs, which i own
    outputs_type _outputs;

    // suppressed metamethods
private:
    // constructors
    Factory(const Factory &) = delete;
    Factory & operator=(const Factory &) = delete;
    Factory(Factory &&) = delete;
    Factory & operator=(Factory &&) = delete;
};

// get the inline definitions
#include "Factory.icc"


// end of file
