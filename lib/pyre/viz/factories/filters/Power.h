// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// map signal to scale * (signal/mean)^exponent
template <class signalT, class powerT>
class pyre::viz::factories::filters::Power : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using power_type = powerT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Power>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using power_ref_type = std::shared_ptr<power_type>;

    // factory
public:
    inline static auto create(const name_type & name, double mean, double scale, double exponent)
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
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

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
