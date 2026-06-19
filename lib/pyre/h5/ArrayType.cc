// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "ArrayType.h"


// adopt an existing raw handle
pyre::h5::ArrayType::ArrayType(id_type id) : DataType(id) {}


// make an array of the given {cell} type and {shape}
pyre::h5::ArrayType::ArrayType(const DataType & cell, const shape_t & shape) :
    DataType(static_cast<id_type>(H5Tarray_create2(cell.id(), shape.size(), shape.data())))
{}


// end of file
