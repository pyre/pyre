// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// map values in [0,1] onto [a,b]
template <class signalT, class affineT>
class pyre::viz::factories::filters::Affine : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
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
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

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
