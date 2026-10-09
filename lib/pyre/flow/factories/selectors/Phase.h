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

// compute the phase of a complex signal, in radians
template <class signalT, class phaseT>
class pyre::flow::factories::selectors::Phase : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Phase<signalT, phaseT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my slots
    using signal_type = signalT;
    using phase_type = phaseT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Phase>;
    // my input slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    // and my output slots
    using phase_ref_type = std::shared_ptr<phase_type>;

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
    virtual ~Phase();
    // constructor: DON'T CALL
    inline Phase(sentinel_type, const name_type &);

    // accessors
public:
    // input slots
    auto signal() -> signal_ref_type;
    // output slots
    auto phase() -> phase_ref_type;

    // mutators
public:
    // input slots
    auto signal(signal_ref_type) -> factory_ref_type;
    // output slots
    auto phase(phase_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    Phase(const Phase &) = delete;
    Phase & operator=(const Phase &) = delete;
    Phase(Phase &&) = delete;
    Phase & operator=(Phase &&) = delete;
};

// get the inline definitions
#include "Phase.icc"


// end of file
