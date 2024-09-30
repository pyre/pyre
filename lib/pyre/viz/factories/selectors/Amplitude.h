// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class signalT, class amplitudeT>
class pyre::viz::factories::selectors::Amplitude : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using signal_type = signalT;
    using amplitude_type = amplitudeT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Amplitude>;
    // my input slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    // and my output slots
    using amplitude_ref_type = std::shared_ptr<amplitude_type>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Amplitude();
    // constructor: DON'T CALL
    inline Amplitude(sentinel_type, const name_type &);

    // accessors
public:
    // input slots
    auto signal() -> signal_ref_type;
    // output slots
    auto amplitude() -> amplitude_ref_type;

    // mutators
public:
    // input slots
    auto signal(signal_ref_type) -> factory_ref_type;
    // output slots
    auto amplitude(amplitude_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    Amplitude(const Amplitude &) = delete;
    Amplitude & operator=(const Amplitude &) = delete;
    Amplitude(Amplitude &&) = delete;
    Amplitude & operator=(Amplitude &&) = delete;
};

// get the inline definitions
#include "Amplitude.icc"

// end of file
