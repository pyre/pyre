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


// an hdf5 variable length datatype
class pyre::h5::types::VarLen : public pyre::h5::types::Datatype {
    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit VarLen(id_type id);
    // make a variable length type whose elements are of the given {cell} type
    explicit VarLen(const Datatype & cell);
    // the full set of special members
    VarLen(const VarLen &) = default;
    VarLen(VarLen &&) noexcept = default;
    VarLen & operator=(const VarLen &) = default;
    VarLen & operator=(VarLen &&) noexcept = default;
    ~VarLen() override = default;
};


// end of file
