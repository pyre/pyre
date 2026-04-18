// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "external.h"
// forward declarations
#include "forward.h"


// the {datatype} specializations
template <>
inline auto
pyre::h5::datatype(const char *) -> const datatype_t &
{
    // build a NATIVE char
    return H5::PredType::NATIVE_CHAR;
}

template <>
inline auto
pyre::h5::datatype(const short *) -> const datatype_t &
{
    // build a NATIVE short
    return H5::PredType::NATIVE_SHORT;
}

template <>
inline auto
pyre::h5::datatype(const int *) -> const datatype_t &
{
    // build a NATIVE int
    return H5::PredType::NATIVE_INT;
}

template <>
inline auto
pyre::h5::datatype(const long *) -> const datatype_t &
{
    // build a NATIVE long
    return H5::PredType::NATIVE_LONG;
}

template <>
inline auto
pyre::h5::datatype(const float *) -> const datatype_t &
{
    // build a NATIVE float
    return H5::PredType::NATIVE_FLOAT;
}

template <>
inline auto
pyre::h5::datatype(const double *) -> const datatype_t &
{
    // build a NATIVE double
    return H5::PredType::NATIVE_DOUBLE;
}


// end of file
