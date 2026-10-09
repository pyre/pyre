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

// cut the signal into sawteeth of width pi/6 and map each one onto [0,1]
template <class signalT, class polarsawT>
class pyre::flow::factories::filters::PolarSaw : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = PolarSaw<signalT, polarsawT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using polarsaw_type = polarsawT;

    // ref to me
    using factory_ref_type = std::shared_ptr<PolarSaw>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using polarsaw_ref_type = std::shared_ptr<polarsaw_type>;

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
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

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
