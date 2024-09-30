// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// map values in [0,1] onto [a,b]
template <class signalT, class polarsawT>
class pyre::viz::factories::filters::PolarSaw : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using polarsaw_type = polarsawT;

    // ref to me
    using factory_ref_type = std::shared_ptr<PolarSaw>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using polarsaw_ref_type = std::shared_ptr<polarsaw_type>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~PolarSaw();
    // constructor; DON'T CALL
    inline PolarSaw(sentinel_type, const name_type &);

    // accessors
public:
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {polarsaw} slot
    auto polarsaw() -> polarsaw_ref_type;

    // mutators
public:
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {polarsaw} slot
    auto polarsaw(polarsaw_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    PolarSaw(const PolarSaw &) = delete;
    PolarSaw & operator=(const PolarSaw &) = delete;
    PolarSaw(PolarSaw &&) = delete;
    PolarSaw & operator=(PolarSaw &&) = delete;
};

// get the inline definitions
#include "PolarSaw.icc"

// end of file
