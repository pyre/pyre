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


// the {datatype} specializations for unsigned integral types
template <>
auto
pyre::h5::datatype<std::uint8_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_UINT8;
}

template <>
auto
pyre::h5::datatype<std::uint16_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_UINT16;
}

template <>
auto
pyre::h5::datatype<std::uint32_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_UINT32;
}

template <>
auto
pyre::h5::datatype<std::uint64_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_UINT64;
}

// the {datatype} specializations for signed integral types
template <>
auto
pyre::h5::datatype<std::int8_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_INT8;
}

template <>
auto
pyre::h5::datatype<std::int16_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_INT16;
}

template <>
auto
pyre::h5::datatype<std::int32_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_INT32;
}

template <>
auto
pyre::h5::datatype<std::int64_t>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_INT64;
}

// floating point types
template <>
auto
pyre::h5::datatype<float>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_FLOAT;
}

template <>
auto
pyre::h5::datatype<double>() -> datatype_t
{
    // build the corresponding NATIVE type
    return H5::PredType::NATIVE_DOUBLE;
}

// complex types
template <>
auto
pyre::h5::datatype<std::complex<float>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_FLOAT;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<double>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_DOUBLE;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint8_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_UINT8;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint16_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_UINT16;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint32_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_UINT32;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::uint64_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_UINT64;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::int8_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_INT8;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::int16_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_INT16;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::int32_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_INT32;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}

template <>
auto
pyre::h5::datatype<std::complex<std::int64_t>>() -> datatype_t
{
    // grab the native base type
    auto base = H5::PredType::NATIVE_INT64;
    // allocate the complex type
    auto complex = H5::CompType(2 * base.getSize());
    // insert the real and imaginary parts
    complex.insertMember("r", 0, base);
    complex.insertMember("i", base.getSize(), base);
    // and return the type
    return complex;
}


// end of file
