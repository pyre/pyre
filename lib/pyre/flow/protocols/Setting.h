// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// the description of a setting of a factory: its name, the type of its values, and how to read
// and change it on a factory without knowing the factory's concrete type; factories describe
// their settings so that an inspector can list them and change them by name
class pyre::flow::protocols::Setting {
    // type aliases
public:
    // me
    using self_type = Setting;
    // the names of settings, and of the types of their values
    using name_type = string_t;
    // the value of a setting, whatever its type
    using value_type = setting_t;
    // how to read a setting of a factory
    using getter_type = std::function<value_type(const Factory &)>;
    // how to change it; false if the value is not of the setting's type
    using setter_type = std::function<bool(Factory &, const value_type &)>;

    // factories
public:
    // describe the setting {name} of factories of type {factoryT}, which read it through {get}
    // and change it through {set}
    template <class factoryT, class valueT, class resultT>
    static inline auto of(
        const name_type & name, valueT (factoryT::*get)() const, resultT (factoryT::*set)(valueT))
        -> self_type;

    // metamethods
public:
    // constructor
    inline Setting(name_type name, name_type type, getter_type get, setter_type set);
    // destructor
    ~Setting() = default;
    // descriptions are values: they copy and move freely
    Setting(const Setting &) = default;
    Setting(Setting &&) = default;
    Setting & operator=(const Setting &) = default;
    Setting & operator=(Setting &&) = default;

    // accessors
public:
    // my name
    inline auto name() const -> const name_type &;
    // the name of the type of my values: "int", "double", or "interval"
    inline auto type() const -> const name_type &;

    // interface
public:
    // read my value on {factory}
    inline auto get(const Factory & factory) const -> value_type;
    // change my value on {factory}; false if {value} is not of my type
    inline auto set(Factory & factory, const value_type & value) const -> bool;

    // implementation details
private:
    // the name of the type {valueT}
    template <class valueT>
    static inline auto typeName() -> name_type;
    // extract a value of type {valueT} from {value}, widening an integer where a floating
    // point value is expected; nothing if {value} holds something else
    template <class valueT>
    static inline auto extract(const value_type & value) -> std::optional<valueT>;

    // implementation details - data
private:
    // my name
    name_type _name;
    // the name of the type of my values
    name_type _type;
    // how to read me
    getter_type _get;
    // how to change me
    setter_type _set;
};

// get the inline definitions
#include "Setting.icc"


// end of file
