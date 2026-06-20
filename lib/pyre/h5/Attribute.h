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


// an hdf5 attribute: a small named value attached to a group, dataset, or named datatype
class pyre::h5::Attribute : public pyre::h5::Identifier {
    // types
public:
    // the class of my datatype: integer, float, string, ...
    using class_type = H5T_class_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Attribute(id_type id);
    // the full set of special members
    Attribute(const Attribute &) = default;
    Attribute(Attribute &&) noexcept = default;
    Attribute & operator=(const Attribute &) = default;
    Attribute & operator=(Attribute &&) noexcept = default;
    ~Attribute() override = default;

    // interface
public:
    // my name
    auto name() const -> string_t;
    // the class of my datatype
    auto cell() const -> class_type;
    // my datatype, as a fresh owned wrapper
    auto datatype() const -> types::Datatype;
    // my dataspace, as a fresh owned wrapper
    auto dataspace() const -> DataSpace;
    // my on-disk size, in bytes
    auto storageSize() const -> hsize_t;
    // my in-memory size, in bytes
    auto memorySize() const -> std::size_t;
    // read my raw value, interpreted as {memtype}, into {buffer}
    auto read(id_type memtype, void * buffer) const -> void;
    // write {buffer}, interpreted as {memtype}, into me
    auto write(id_type memtype, const void * buffer) const -> void;
    // read my value as a string
    auto readString() const -> string_t;
    // write {value} into me as a string
    auto writeString(const string_t & value) const -> void;
    // release my handle
    auto close() -> void;
};


// end of file
