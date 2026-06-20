// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Identifier.h"


// an hdf5 location: anything that can carry attributes — a group, dataset, or named datatype
class pyre::h5::Location : public pyre::h5::Identifier {
    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Location(id_type id);
    // the full set of special members
    Location(const Location &) = default;
    Location(Location &&) noexcept = default;
    Location & operator=(const Location &) = default;
    Location & operator=(Location &&) noexcept = default;
    ~Location() override = default;

    // attribute interface
public:
    // the number of attributes i carry
    auto attributeCount() const -> int;
    // the attribute at the given {index}
    auto openAttribute(unsigned int index) const -> Attribute;
    // the attribute by the given {name}
    auto openAttribute(const string_t & name) const -> Attribute;
    // whether i carry an attribute by the given {name}
    auto hasAttribute(const string_t & name) const -> bool;
    // create an attribute {name} of {type} over {space}, with creation property list {acpl}
    auto createAttribute(
        const string_t & name, const types::Datatype & type, const DataSpace & space,
        const properties::List & acpl) const -> Attribute;
    // rename the {oldName} attribute to {newName}
    auto renameAttribute(const string_t & oldName, const string_t & newName) const -> void;
    // remove the attribute by the given {name}
    auto removeAttribute(const string_t & name) const -> void;
};


// end of file
