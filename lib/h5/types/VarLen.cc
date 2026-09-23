// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "VarLen.h"
// the reporting of library refusals
#include "../diagnostics.h"


// adopt an existing raw handle
pyre::h5::types::VarLen::VarLen(id_type id) : Datatype(id) {}


// make a variable length type whose elements are of the given {cell} type
pyre::h5::types::VarLen::VarLen(const Datatype & cell) :
    Datatype(static_cast<id_type>(H5Tvlen_create(cell.id())))
{
    // if the library refused
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "creating a variable length datatype");
    }
}


// end of file
