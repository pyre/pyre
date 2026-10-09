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
// the magnitude of a cell of any type
#include "../../utilities.h"

// compute the amplitude of a complex signal
template <class signalT, class amplitudeT>
class pyre::flow::factories::selectors::Amplitude : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Amplitude<signalT, amplitudeT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my slots
    using signal_type = signalT;
    using amplitude_type = amplitudeT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Amplitude>;
    // my input slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    // and my output slots
    using amplitude_ref_type = std::shared_ptr<amplitude_type>;

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
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

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
