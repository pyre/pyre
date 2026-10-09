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

// keep every 2^level cell of the signal along each axis
template <class signalT>
class pyre::flow::factories::filters::Decimate : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Decimate<signalT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // both input and output slots are the same type
    using signal_type = signalT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Decimate>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;

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
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

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
