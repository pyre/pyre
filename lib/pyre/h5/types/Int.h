// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Atom.h"


// an hdf5 integer datatype
class pyre::h5::types::Int : public pyre::h5::types::Atom {
    // types
public:
    // whether i am signed or unsigned
    using sign_type = H5T_sign_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Int(id_type id);
    // make an independent copy of a predefined integer type
    explicit Int(const Predefined & type);
    // the full set of special members
    Int(const Int &) = default;
    Int(Int &&) noexcept = default;
    Int & operator=(const Int &) = default;
    Int & operator=(Int &&) noexcept = default;
    ~Int() override = default;

    // interface
public:
    // my sign type
    auto sign() const -> sign_type;
    // set my sign type
    auto setSign(sign_type sign) -> void;
};


// end of file
