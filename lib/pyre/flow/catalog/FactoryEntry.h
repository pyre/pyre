// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// the factories i make
#include "../protocols/Factory.h"


// what the catalog knows about a kind of factory: the declaration of its type, a readable name,
// the descriptions of its slots and settings, which a palette and an inspector can show before
// any factory of this kind exists, and how to make one with a given name
class pyre::flow::catalog::FactoryEntry {
    // type aliases
public:
    // me
    using self_type = FactoryEntry;
    // the declarations of types, and the names of things
    using decl_type = string_t;
    using name_type = string_t;
    // the descriptions of the slots and the settings of my factories
    using slots_type = protocols::Factory::slots_type;
    using settings_type = protocols::Factory::settings_type;
    // the factories i make
    using factory_ref_type = std::shared_ptr<protocols::Factory>;
    // how to make one
    using maker_type = std::function<factory_ref_type(const name_type &)>;

    // metamethods
public:
    // constructor
    inline FactoryEntry(
        decl_type decl, name_type className, slots_type slots, settings_type settings,
        maker_type make);
    // destructor
    ~FactoryEntry() = default;
    // entries are values: they copy and move freely
    FactoryEntry(const FactoryEntry &) = default;
    FactoryEntry(FactoryEntry &&) = default;
    FactoryEntry & operator=(const FactoryEntry &) = default;
    FactoryEntry & operator=(FactoryEntry &&) = default;

    // accessors
public:
    // the declaration of the type of my factories, which is my key in the catalog
    inline auto decl() const -> const decl_type &;
    // the readable name of their class
    inline auto className() const -> const name_type &;
    // the descriptions of their slots
    inline auto slots() const -> const slots_type &;
    // the descriptions of their settings
    inline auto settings() const -> const settings_type &;

    // interface
public:
    // make a factory named {name}
    inline auto make(const name_type & name) const -> factory_ref_type;

    // implementation details - data
private:
    // the declaration of the type of my factories
    decl_type _decl;
    // the readable name of their class
    name_type _className;
    // the descriptions of their slots
    slots_type _slots;
    // the descriptions of their settings
    settings_type _settings;
    // how to make one
    maker_type _make;
};

// get the inline definitions
#include "FactoryEntry.icc"


// end of file
