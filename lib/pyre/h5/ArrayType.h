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


// an hdf5 array datatype
class pyre::h5::ArrayType : public pyre::h5::DataType {
    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit ArrayType(id_type id);
    // make an array of the given {cell} type and {shape}
    ArrayType(const DataType & cell, const shape_t & shape);
    // the full set of special members
    ArrayType(const ArrayType &) = default;
    ArrayType(ArrayType &&) noexcept = default;
    ArrayType & operator=(const ArrayType &) = default;
    ArrayType & operator=(ArrayType &&) noexcept = default;
    ~ArrayType() override = default;
};


// end of file
