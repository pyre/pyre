// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "../Identifier.h"


// the generic base of the hdf5 property lists
class pyre::h5::properties::List : public pyre::h5::Identifier {
    // metamethods
public:
    // the default property list, a handle to the library-wide defaults
    List();
    // the full set of special members
    List(const List &) = default;
    List(List &&) noexcept = default;
    List & operator=(const List &) = default;
    List & operator=(List &&) noexcept = default;
    ~List() override = default;

    // interface
public:
    // the number of properties in the list
    auto numProps() const -> std::size_t;
    // whether the list has a property by the given {name}
    auto exists(const string_t & name) const -> bool;
    // the size, in bytes, of the property by the given {name}
    auto propertySize(const string_t & name) const -> std::size_t;
    // the value of the property by the given {name}, as raw bytes in a string
    auto property(const string_t & name) const -> string_t;
    // set the property by the given {name} to {value}
    auto setProperty(const string_t & name, const string_t & value) -> void;
    // remove the property by the given {name}
    auto removeProperty(const string_t & name) -> void;
    // release my handle
    auto close() -> void;

    // implementation details
protected:
    // adopt an existing raw handle; for derived lists to pass a freshly created one
    explicit List(id_type id);
};


// end of file
