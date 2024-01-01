// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// map values in [0,1] into uniformly spaced bins: [0,1) -> Z_bins
template <class signalT, class binT>
class pyre::viz::factories::filters::Uniform : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using bin_type = binT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Uniform>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using bin_ref_type = std::shared_ptr<bin_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", int bins = 10) -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Uniform();
    // constructor; DON'T CALL
    inline Uniform(sentinel_type, const name_type &, int);

    // accessors
public:
    // get the number of bins
    auto bins() const -> int;
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {bin} slot
    auto bin() -> bin_ref_type;

    // mutators
public:
    // set the number of bins
    auto bins(int bins) -> factory_ref_type;
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {bin} slot
    auto bin(bin_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // implementation details
private:
    // the number of bins
    int _bins;

    // suppressed metamethods
private:
    // constructors
    Uniform(const Uniform &) = delete;
    Uniform & operator=(const Uniform &) = delete;
    Uniform(Uniform &&) = delete;
    Uniform & operator=(Uniform &&) = delete;
};

// get the inline definitions
#include "Uniform.icc"

// end of file
