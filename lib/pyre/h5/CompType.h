// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "DataType.h"


// an hdf5 compound datatype
class pyre::h5::CompType : public pyre::h5::DataType {
    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit CompType(id_type id);
    // make a fresh compound type of the given {size}, in bytes
    explicit CompType(std::size_t size);
    // the full set of special members
    CompType(const CompType &) = default;
    CompType(CompType &&) noexcept = default;
    CompType & operator=(const CompType &) = default;
    CompType & operator=(CompType &&) noexcept = default;
    ~CompType() override = default;

    // interface
public:
    // the number of members i have
    auto members() const -> int;
    // the name of the member at {index}
    auto memberName(unsigned int index) const -> string_t;
    // the index of the member by the given {name}
    auto memberIndex(const string_t & name) const -> int;
    // the byte offset of the member at {index}
    auto memberOffset(unsigned int index) const -> std::size_t;
    // the class of the member at {index}
    auto memberClass(unsigned int index) const -> class_type;
    // the type of the member at {index}, as a fresh handle the caller adopts
    auto memberType(unsigned int index) const -> id_type;
    // insert {name} of {type} at the given {offset}
    auto insert(const string_t & name, std::size_t offset, const DataType & type) -> void;
    // recursively remove padding from within me
    auto pack() -> void;
};


// end of file
