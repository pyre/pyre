// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "VarLenType.h"


// adopt an existing raw handle
pyre::h5::VarLenType::VarLenType(id_type id) : DataType(id) {}


// make a variable length type whose elements are of the given {cell} type
pyre::h5::VarLenType::VarLenType(const DataType & cell) :
    DataType(static_cast<id_type>(H5Tvlen_create(cell.id())))
{}


// end of file
