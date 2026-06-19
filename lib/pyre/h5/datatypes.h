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
// the types i build
#include "types/Datatype.h"
#include "types/Compound.h"


// implementation details for deducing the {datatype} of a cell
namespace pyre::h5 {
    // wrap a fresh, owned copy of a predefined native type
    inline auto
    nativeDatatype(hid_t native) -> datatype_t
    {
        // copy the library constant into a transient i own, and adopt the handle
        return datatype_t(static_cast<hid_t>(H5Tcopy(native)));
    }

    // build a compound {(r, i)} type over the given native base type
    inline auto
    complexDatatype(hid_t native) -> datatype_t
    {
        // grab a fresh copy of the native base type
        auto base = nativeDatatype(native);
        // allocate a compound type wide enough for the two parts
        auto complex = comptype_t(2 * base.bytes());
        // insert the real and imaginary parts
        complex.insert("r", 0, base);
        complex.insert("i", base.bytes(), base);
        // and report it as my base type
        return complex;
    }
} // namespace pyre::h5


// the {datatype} specializations for unsigned integral types
template <>
auto
pyre::h5::datatype<std::uint8_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_UINT8);
}

template <>
auto
pyre::h5::datatype<std::uint16_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_UINT16);
}

template <>
auto
pyre::h5::datatype<std::uint32_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_UINT32);
}

template <>
auto
pyre::h5::datatype<std::uint64_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_UINT64);
}

// the {datatype} specializations for signed integral types
template <>
auto
pyre::h5::datatype<std::int8_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_INT8);
}

template <>
auto
pyre::h5::datatype<std::int16_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_INT16);
}

template <>
auto
pyre::h5::datatype<std::int32_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_INT32);
}

template <>
auto
pyre::h5::datatype<std::int64_t>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_INT64);
}

// floating point types
template <>
auto
pyre::h5::datatype<float>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_FLOAT);
}

template <>
auto
pyre::h5::datatype<double>() -> datatype_t
{
    return nativeDatatype(H5T_NATIVE_DOUBLE);
}

// complex types
template <>
auto
pyre::h5::datatype<std::complex<float>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_FLOAT);
}

template <>
auto
pyre::h5::datatype<std::complex<double>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_DOUBLE);
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint8_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_UINT8);
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint16_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_UINT16);
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint32_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_UINT32);
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint64_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_UINT64);
}

template <>
auto
pyre::h5::datatype<std::complex<std::int8_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_INT8);
}

template <>
auto
pyre::h5::datatype<std::complex<std::int16_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_INT16);
}

template <>
auto
pyre::h5::datatype<std::complex<std::int32_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_INT32);
}

template <>
auto
pyre::h5::datatype<std::complex<std::int64_t>>() -> datatype_t
{
    return complexDatatype(H5T_NATIVE_INT64);
}


// end of file
