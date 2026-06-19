// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Datatype.h"


// an hdf5 enumeration datatype
class pyre::h5::types::Enum : public pyre::h5::types::Datatype {
    // metamethods
public:
    // make an empty enumeration type with no handle yet
    Enum();
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Enum(id_type id);
    // the full set of special members
    Enum(const Enum &) = default;
    Enum(Enum &&) noexcept = default;
    Enum & operator=(const Enum &) = default;
    Enum & operator=(Enum &&) noexcept = default;
    ~Enum() override = default;

    // interface
public:
    // the number of members i have
    auto members() const -> int;
    // the value of the member at {index}
    auto memberValue(unsigned int index) const -> long;
    // the name of the member with the given {value}
    auto nameOf(long value) const -> string_t;
};


// end of file
