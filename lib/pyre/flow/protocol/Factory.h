// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

class pyre::flow::protocol::Factory : public Node {
    // type aliases
public:
    // connectors
    using connectors_type = std::map<name_type, product_ref_type>;

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
    // look up the product bound to an input {slot}
    inline auto input(const name_type & slot) const -> product_ref_type;
    // look up the product bound to an output {slot}
    inline auto output(const name_type & slot) const -> product_ref_type;

    // access to the full set of bindings
    inline auto inputs() const -> const connectors_type &;
    inline auto outputs() const -> const connectors_type &;

    // flow protocol
public:
    // bindings
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
    connectors_type _inputs;
    connectors_type _outputs;

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