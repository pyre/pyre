// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// map values in [0,1] onto [a,b]
template <class signalT, class logsawT>
class pyre::viz::factories::filters::LogSaw : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slot
    using signal_type = signalT;
    // my output slot
    using logsaw_type = logsawT;

    // ref to me
    using factory_ref_type = std::shared_ptr<LogSaw>;
    // and to my products
    using signal_ref_type = std::shared_ptr<signal_type>;
    using logsaw_ref_type = std::shared_ptr<logsaw_type>;

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
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

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
