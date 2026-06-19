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


// an hdf5 variable length datatype
class pyre::h5::VarLenType : public pyre::h5::DataType {
    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit VarLenType(id_type id);
    // make a variable length type whose elements are of the given {cell} type
    explicit VarLenType(const DataType & cell);
    // the full set of special members
    VarLenType(const VarLenType &) = default;
    VarLenType(VarLenType &&) noexcept = default;
    VarLenType & operator=(const VarLenType &) = default;
    VarLenType & operator=(VarLenType &&) noexcept = default;
    ~VarLenType() override = default;
};


// end of file
