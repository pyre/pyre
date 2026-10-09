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

// map values in [0,1] onto [a,b]
template <class signalT, class affineT>
class pyre::flow::factories::filters::Affine : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Affine<signalT, affineT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my interval
    using interval_type = interval_t;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using affine_type = affineT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Affine>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using affine_ref_type = std::shared_ptr<affine_type>;

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
    inline static auto create(const name_type & name = "", interval_type interval = { 0, 1 })
        -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Affine();
    // constructor; DON'T CALL
    inline Affine(sentinel_type, const name_type &, interval_type);

    // accessors
public:
    // get the interval
    auto interval() const -> interval_type;
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {affine} slot
    auto affine() -> affine_ref_type;

    // mutators
public:
    // set the interval
    auto interval(interval_type interval) -> factory_ref_type;
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {affine} slot
    auto affine(affine_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // implementation details
private:
    // the interval
    interval_type _interval;

    // suppressed metamethods
private:
    // constructors
    Affine(const Affine &) = delete;
    Affine & operator=(const Affine &) = delete;
    Affine(Affine &&) = delete;
    Affine & operator=(Affine &&) = delete;
};

// get the inline definitions
#include "Affine.icc"


// end of file
