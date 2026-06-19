// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "IntType.h"
// the predefined type i can copy
#include "PredType.h"


// adopt an existing raw handle
pyre::h5::IntType::IntType(id_type id) : AtomType(id) {}


// make an independent copy of a predefined integer type
pyre::h5::IntType::IntType(const PredType & type) :
    AtomType(static_cast<id_type>(H5Tcopy(type.id())))
{}


// my sign type
auto
pyre::h5::IntType::sign() const -> sign_type
{
    // ask the library
    return H5Tget_sign(id());
}


// set my sign type
auto
pyre::h5::IntType::setSign(sign_type sign) -> void
{
    // hand it to the library
    H5Tset_sign(id(), sign);
    // all done
    return;
}


// end of file
