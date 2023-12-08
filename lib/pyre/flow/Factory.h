// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::flow::Factory : public Node {
    // type aliases
public:
    // connectors
    using connectors_type = std::map<name_type, product_ref_type>;

    // metamethods
protected:
    // constructors
    inline Factory(sentinel_type);

    // accessors
public:
    inline auto inputs() const -> const connectors_type &;
    inline auto outputs() const -> const connectors_type &;

    // interface
public:
    // look up the product bound to an input {slot}
    inline auto input(const name_type & slot) -> product_ref_type;
    // look up the product bound to an output {slot}
    inline auto output(const name_type & name) -> product_ref_type;

    // invalidate me
    virtual auto flush() -> void override;
    // rebuild the product connected to one of my slots
    virtual auto refresh(name_type slot, product_ref_type product) -> void;

    // implementation details - data
private:
    connectors_type _inputs;
    connectors_type _outputs;

    // default metamethods
public:
    // destructor
    virtual ~Factory() = default;

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