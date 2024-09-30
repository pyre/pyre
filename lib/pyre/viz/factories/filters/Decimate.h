// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// generate a tile filled with a value
template <class signalT>
class pyre::viz::factories::filters::Decimate : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // both input and output sl;ots are the same type
    using signal_type = signalT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Decimate>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", int level = 0) -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Decimate();
    // constructor; DON'T CALL
    inline Decimate(sentinel_type, const name_type &, int);

    // accessors
public:
    // get the zoom factor
    auto level() const -> int;
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {decimated} slot
    auto decimated() -> signal_ref_type;

    // mutators
public:
    // set the zoom factor
    auto level(int level) -> factory_ref_type;
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {decimated} slot
    auto decimated(signal_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // implementation details
private:
    int _level;

    // suppressed metamethods
private:
    // constructors
    Decimate(const Decimate &) = delete;
    Decimate & operator=(const Decimate &) = delete;
    Decimate(Decimate &&) = delete;
    Decimate & operator=(Decimate &&) = delete;
};

// get the inline definitions
#include "Decimate.icc"

// end of file
