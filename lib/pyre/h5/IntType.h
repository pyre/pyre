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


// an hdf5 integer datatype
class pyre::h5::IntType : public pyre::h5::AtomType {
    // types
public:
    // whether i am signed or unsigned
    using sign_type = H5T_sign_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit IntType(id_type id);
    // make an independent copy of a predefined integer type
    explicit IntType(const PredType & type);
    // the full set of special members
    IntType(const IntType &) = default;
    IntType(IntType &&) noexcept = default;
    IntType & operator=(const IntType &) = default;
    IntType & operator=(IntType &&) noexcept = default;
    ~IntType() override = default;

    // interface
public:
    // my sign type
    auto sign() const -> sign_type;
    // set my sign type
    auto setSign(sign_type sign) -> void;
};


// end of file
