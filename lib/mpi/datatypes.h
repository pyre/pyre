// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the generic case
//
// mpi can only move cells whose layout it knows, so there is no sensible answer for an
// arbitrary {cellT}. the assertion below is worded in terms of {cellT} so that it fires only
// when somebody actually asks for an unsupported type, rather than when this template is parsed
template <typename cellT>
inline auto
pyre::mpi::datatype() -> datatype_t
{
    // refuse, at compile time, to guess
    static_assert(
        sizeof(cellT) == 0, "pyre::mpi::datatype: mpi does not know the layout of this type");
    // unreachable; here only so the return type checks out
    return MPI_DATATYPE_NULL;
}


// the signed fixed width integral types
template <>
inline auto
pyre::mpi::datatype<std::int8_t>() -> datatype_t
{
    // a byte wide signed integer
    return MPI_INT8_T;
}

template <>
inline auto
pyre::mpi::datatype<std::int16_t>() -> datatype_t
{
    // a two byte signed integer
    return MPI_INT16_T;
}

template <>
inline auto
pyre::mpi::datatype<std::int32_t>() -> datatype_t
{
    // a four byte signed integer
    return MPI_INT32_T;
}

template <>
inline auto
pyre::mpi::datatype<std::int64_t>() -> datatype_t
{
    // an eight byte signed integer
    return MPI_INT64_T;
}


// the unsigned fixed width integral types
template <>
inline auto
pyre::mpi::datatype<std::uint8_t>() -> datatype_t
{
    // a byte wide unsigned integer
    return MPI_UINT8_T;
}

template <>
inline auto
pyre::mpi::datatype<std::uint16_t>() -> datatype_t
{
    // a two byte unsigned integer
    return MPI_UINT16_T;
}

template <>
inline auto
pyre::mpi::datatype<std::uint32_t>() -> datatype_t
{
    // a four byte unsigned integer
    return MPI_UINT32_T;
}

template <>
inline auto
pyre::mpi::datatype<std::uint64_t>() -> datatype_t
{
    // an eight byte unsigned integer
    return MPI_UINT64_T;
}


// the floating point types
template <>
inline auto
pyre::mpi::datatype<float>() -> datatype_t
{
    // single precision
    return MPI_FLOAT;
}

template <>
inline auto
pyre::mpi::datatype<double>() -> datatype_t
{
    // double precision
    return MPI_DOUBLE;
}

template <>
inline auto
pyre::mpi::datatype<long double>() -> datatype_t
{
    // whatever extended precision this platform offers
    return MPI_LONG_DOUBLE;
}


// the complex types; the {MPI_CXX_} spellings are the ones that match the layout of
// {std::complex}, and they have been in the standard since mpi 3.0
template <>
inline auto
pyre::mpi::datatype<std::complex<float>>() -> datatype_t
{
    // a pair of single precision reals
    return MPI_CXX_FLOAT_COMPLEX;
}

template <>
inline auto
pyre::mpi::datatype<std::complex<double>>() -> datatype_t
{
    // a pair of double precision reals
    return MPI_CXX_DOUBLE_COMPLEX;
}


// the character and truth types; each is a distinct type from every fixed width integral
// above, so neither collides with the specializations at the top of this file
template <>
inline auto
pyre::mpi::datatype<char>() -> datatype_t
{
    // a character, whose signedness is up to the platform
    return MPI_CHAR;
}

template <>
inline auto
pyre::mpi::datatype<bool>() -> datatype_t
{
    // a truth value laid out the way c++ lays it out
    return MPI_CXX_BOOL;
}


// raw memory, which mpi moves without interpreting
template <>
inline auto
pyre::mpi::datatype<std::byte>() -> datatype_t
{
    // an uninterpreted octet
    return MPI_BYTE;
}


// end of file
