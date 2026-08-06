// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "ACPL.h"


// make a fresh attribute creation property list
pyre::h5::properties::ACPL::ACPL() : STRCPL(H5Pcreate(H5P_ATTRIBUTE_CREATE)) {}


// adopt an existing raw handle
pyre::h5::properties::ACPL::ACPL(id_type id) : STRCPL(id) {}


// the shared default attribute creation property list
auto
pyre::h5::properties::ACPL::theDefault() -> const ACPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const ACPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// end of file
