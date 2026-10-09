// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "../../protocols/Factory.h"

// generate a tile filled with a value
template <class constantT>
class pyre::flow::factories::filters::Constant : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Constant<constantT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my product
    using product_type = constantT;
    // my value type
    using cell_type = typename product_type::cell_type;

    // ref to me
    using factory_ref_type = std::shared_ptr<Constant>;
    // and to my products
    using product_ref_type = std::shared_ptr<product_type>;

    // the spelling of types
    using string_type = string_t;

    // the spelling of my type, and the descriptions of my slots and settings
public:
    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // the human readable form of my class name
    static inline auto className() -> string_type;
    // the descriptions of my slots, shared by every factory of my type
    static inline auto declSlots() -> const slots_type &;
    // the descriptions of my settings, shared by every factory of my type
    static inline auto declSettings() -> const settings_type &;

    // introspection
public:
    // the descriptions of my slots
    inline virtual auto slots() const -> const slots_type & override;
    // the descriptions of my settings
    inline virtual auto settings() const -> const settings_type & override;

    // factory
public:
    inline static auto create(const name_type & name = "", cell_type value = 0) -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Constant();
    // constructor; DON'T CALL
    inline Constant(sentinel_type, const name_type &, cell_type);

    // accessors
public:
    // get the tile fill value
    auto value() const -> cell_type;
    // get the product bound to my {tile} slot
    auto tile() -> product_ref_type;

    // mutators
public:
    // set the tile fill value
    auto value(cell_type value) -> factory_ref_type;
    // set the product bound to my {tile} slot
    auto tile(product_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // implementation details
private:
    cell_type _value;

    // suppressed metamethods
private:
    // constructors
    Constant(const Constant &) = delete;
    Constant & operator=(const Constant &) = delete;
    Constant(Constant &&) = delete;
    Constant & operator=(Constant &&) = delete;
};

// get the inline definitions
#include "Constant.icc"


// end of file
