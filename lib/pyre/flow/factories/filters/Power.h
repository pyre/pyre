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

// map signal to scale * (signal/mean)^exponent
template <class signalT, class powerT>
class pyre::flow::factories::filters::Power : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Power<signalT, powerT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using power_type = powerT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Power>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using power_ref_type = std::shared_ptr<power_type>;

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
    inline static auto create(
        const name_type & name = "", double mean = 1, double scale = 1, double exponent = 1)
        -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Power();
    // constructor; DON'T CALL
    inline Power(sentinel_type, const name_type &, double mean, double scale, double exponent);

    // accessors
public:
    // get the mean
    auto mean() const -> double;
    // get the mean
    auto scale() const -> double;
    // get the mean
    auto exponent() const -> double;
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {power} slot
    auto power() -> power_ref_type;

    // mutators
public:
    // set the mean
    auto mean(double mean) -> factory_ref_type;
    // set the scale
    auto scale(double scale) -> factory_ref_type;
    // set the exponent
    auto exponent(double exponent) -> factory_ref_type;
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {power} slot
    auto power(power_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // implementation detail
private:
    double _mean;
    double _scale;
    double _exponent;

    // suppressed metamethods
private:
    // constructors
    Power(const Power &) = delete;
    Power & operator=(const Power &) = delete;
    Power(Power &&) = delete;
    Power & operator=(Power &&) = delete;
};

// get the inline definitions
#include "Power.icc"


// end of file
