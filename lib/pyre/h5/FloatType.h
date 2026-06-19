// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "AtomType.h"


// an hdf5 floating point datatype
class pyre::h5::FloatType : public pyre::h5::AtomType {
    // types
public:
    // the mantissa normalization strategy
    using norm_type = H5T_norm_t;
    // the strategy for filling internal unused bits
    using pad_type = H5T_pad_t;
    // the bit layout: (sign pos, exponent pos, exponent size, mantissa pos, mantissa size)
    using fields_type = std::tuple<std::size_t, std::size_t, std::size_t, std::size_t, std::size_t>;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit FloatType(id_type id);
    // make an independent copy of a predefined float type
    explicit FloatType(const PredType & type);
    // the full set of special members
    FloatType(const FloatType &) = default;
    FloatType(FloatType &&) noexcept = default;
    FloatType & operator=(const FloatType &) = default;
    FloatType & operator=(FloatType &&) noexcept = default;
    ~FloatType() override = default;

    // interface
public:
    // my exponent bias
    auto bias() const -> std::size_t;
    // set my exponent bias
    auto setBias(std::size_t bias) -> void;
    // my mantissa normalization strategy
    auto normalization() const -> norm_type;
    // set my mantissa normalization strategy
    auto setNorm(norm_type norm) -> void;
    // my internal padding strategy
    auto inpad() const -> pad_type;
    // set my internal padding strategy
    auto setInpad(pad_type pad) -> void;
    // my bit layout
    auto fields() const -> fields_type;
    // set my bit layout
    auto setFields(
        std::size_t spos, std::size_t epos, std::size_t esize, std::size_t mpos,
        std::size_t msize) -> void;
};


// end of file
