// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "PredType.h"


// wrap a predefined-type constant
pyre::h5::PredType::PredType(id_type id) : AtomType(id)
{
    // these are immutable globals the library owns forever; take out a reference of my own so my
    // {Identifier} bookkeeping stays balanced and i never drive the count below the library's
    _retain();
}


// end of file
