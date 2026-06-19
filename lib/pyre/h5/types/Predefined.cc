// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Predefined.h"


// wrap a predefined-type constant
pyre::h5::types::Predefined::Predefined(id_type id) : Atom(id)
{
    // these are immutable globals the library owns forever; take out a reference of my own so my
    // {Identifier} bookkeeping stays balanced and i never drive the count below the library's
    _retain();
}


// end of file
