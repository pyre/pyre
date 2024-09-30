// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class signalT, class realT>
class pyre::viz::factories::selectors::Real : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using signal_type = signalT;
    using real_type = realT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Real>;
    // my input slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    // and my output slots
    using real_ref_type = std::shared_ptr<real_type>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Real();
    // constructor: DON'T CALL
    inline Real(sentinel_type, const name_type &);

    // accessors
public:
    // input slots
    auto signal() -> signal_ref_type;
    // output slots
    auto real() -> real_ref_type;

    // mutators
public:
    // input slots
    auto signal(signal_ref_type) -> factory_ref_type;
    // output slots
    auto real(real_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    Real(const Real &) = delete;
    Real & operator=(const Real &) = delete;
    Real(Real &&) = delete;
    Real & operator=(Real &&) = delete;
};

// get the inline definitions
#include "Real.icc"

// end of file
