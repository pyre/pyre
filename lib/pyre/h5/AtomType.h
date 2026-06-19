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


// the base of the hdf5 atomic datatypes: integers, floats, strings, ...
class pyre::h5::AtomType : public pyre::h5::DataType {
    // types
public:
    // the byte order of my representation
    using order_type = H5T_order_t;
    // the bit padding strategy at my boundaries
    using pad_type = H5T_pad_t;
    // a (least significant, most significant) pair of padding strategies
    using padding_type = std::pair<pad_type, pad_type>;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit AtomType(id_type id);
    // the full set of special members
    AtomType(const AtomType &) = default;
    AtomType(AtomType &&) noexcept = default;
    AtomType & operator=(const AtomType &) = default;
    AtomType & operator=(AtomType &&) noexcept = default;
    ~AtomType() override = default;

    // interface
public:
    // my byte order
    auto order() const -> order_type;
    // set my byte order
    auto setOrder(order_type order) -> void;
    // the bit offset of my first significant bit
    auto offset() const -> std::size_t;
    // set the bit offset of my first significant bit
    auto setOffset(std::size_t offset) -> void;
    // my (lsb, msb) padding strategy
    auto pad() const -> padding_type;
    // set my (lsb, msb) padding strategy
    auto setPad(pad_type lsb, pad_type msb) -> void;
    // my precision, in bits
    auto precision() const -> std::size_t;
    // set my precision, in bits
    auto setPrecision(std::size_t precision) -> void;
};


// end of file
