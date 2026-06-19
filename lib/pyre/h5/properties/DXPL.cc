// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DXPL.h"


// make a fresh dataset memory transfer property list
pyre::h5::properties::DXPL::DXPL() : List(H5Pcreate(H5P_DATASET_XFER)) {}


// make one that applies the given data transform {expression}
pyre::h5::properties::DXPL::DXPL(const string_t & expression) : List(H5Pcreate(H5P_DATASET_XFER))
{
    // install the transform
    H5Pset_data_transform(id(), expression.data());
}


// adopt an existing raw handle
pyre::h5::properties::DXPL::DXPL(id_type id) : List(id) {}


// the shared default dataset memory transfer property list
auto
pyre::h5::properties::DXPL::theDefault() -> const DXPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const DXPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// end of file
