// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// map values in [0,1] onto [a,b]
template <class signalT, class cycleT>
class pyre::viz::factories::filters::Cycle : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my interval
    using interval_type = interval_t;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using cycle_type = cycleT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Cycle>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using cycle_ref_type = std::shared_ptr<cycle_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", interval_type interval = { 0, 1 })
        -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Cycle();
    // constructor; DON'T CALL
    inline Cycle(sentinel_type, const name_type &, interval_type);

    // accessors
public:
    // get the interval
    auto interval() const -> interval_type;
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {cycle} slot
    auto cycle() -> cycle_ref_type;

    // mutators
public:
    // set the interval
    auto interval(interval_type interval) -> factory_ref_type;
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {cycle} slot
    auto cycle(cycle_ref_type) -> factory_ref_type;

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
    Cycle(const Cycle &) = delete;
    Cycle & operator=(const Cycle &) = delete;
    Cycle(Cycle &&) = delete;
    Cycle & operator=(Cycle &&) = delete;
};

// get the inline definitions
#include "Cycle.icc"

// end of file
