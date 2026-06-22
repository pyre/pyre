// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class; datatypes can be named (committed) objects that carry attributes
#include "../Location.h"


// the generic base of the hdf5 datatypes
class pyre::h5::types::Datatype : public pyre::h5::Location {
    // types
public:
    // the class of a datatype: integer, float, string, compound, ...
    using class_type = H5T_class_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Datatype(id_type id);
    // make an independent copy of a predefined type
    explicit Datatype(const Predefined & type);
    // the full set of special members
    Datatype(const Datatype &) = default;
    Datatype(Datatype &&) noexcept = default;
    Datatype & operator=(const Datatype &) = default;
    Datatype & operator=(Datatype &&) noexcept = default;
    ~Datatype() override = default;

    // operators
public:
    // whether i describe the same datatype as {other}
    auto operator==(const Datatype & other) const -> bool;
    // whether i describe a different datatype than {other}
    auto operator!=(const Datatype & other) const -> bool;

    // interface
public:
    // the name of my class, for diagnostics
    virtual auto className() const -> string_t;
    // my class: integer, float, string, ...
    auto cell() const -> class_type;
    // my size, in bytes
    auto bytes() const -> std::size_t;
    // resize me to {size} bytes
    auto setBytes(std::size_t size) -> void;
    // the base type from which i am derived
    auto super() const -> Datatype;
    // whether i am, or contain, a member of the given {cls}
    auto isA(class_type cls) const -> bool;
    // a binary description of me, as raw bytes in a string
    auto encode() const -> string_t;
    // the type described by the binary {buffer}
    auto decode(const string_t & buffer) const -> Datatype;
    // release my handle
    auto close() -> void;
};


// end of file
