// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Int.h"
// the predefined type i can copy
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::Int::Int(id_type id) : Atom(id) {}


// make an independent copy of a predefined integer type
pyre::h5::types::Int::Int(const Predefined & type) : Atom(static_cast<id_type>(H5Tcopy(type.id())))
{}


// my sign type
auto
pyre::h5::types::Int::sign() const -> sign_type
{
    // ask the library
    return H5Tget_sign(id());
}


// set my sign type
auto
pyre::h5::types::Int::setSign(sign_type sign) -> void
{
    // hand it to the library
    H5Tset_sign(id(), sign);
    // all done
    return;
}


// end of file
