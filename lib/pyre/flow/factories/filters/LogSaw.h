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

// map the fractional part of the log of the signal magnitude onto [0,1]
template <class signalT, class logsawT>
class pyre::flow::factories::filters::LogSaw : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = LogSaw<signalT, logsawT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using logsaw_type = logsawT;

    // ref to me
    using factory_ref_type = std::shared_ptr<LogSaw>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using logsaw_ref_type = std::shared_ptr<logsaw_type>;

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
    inline virtual ~LogSaw();
    // constructor; DON'T CALL
    inline LogSaw(sentinel_type, const name_type &);

    // accessors
public:
    // get the product bound to my {signal} slot
    auto signal() -> signal_ref_type;
    // get the product bound to my {logsaw} slot
    auto logsaw() -> logsaw_ref_type;

    // mutators
public:
    // set the product bound to my {signal} slot
    auto signal(signal_ref_type) -> factory_ref_type;
    // set the product bound to my {logsaw} slot
    auto logsaw(logsaw_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    LogSaw(const LogSaw &) = delete;
    LogSaw & operator=(const LogSaw &) = delete;
    LogSaw(LogSaw &&) = delete;
    LogSaw & operator=(LogSaw &&) = delete;
};

// get the inline definitions
#include "LogSaw.icc"


// end of file
