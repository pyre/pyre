// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package globla declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// encapsulations of the native datatypes
void
pyre::h5::py::datatypes::native(py::module & m)
{
    // make a new namespace to hold native datatype descriptions
    auto native = m.def_submodule(
        // the name of the module
        "native",
        // its docstring
        "a collection of native types");

    // integral
    native.attr("char") = PredType(H5T_NATIVE_CHAR);
    native.attr("signedChar") = PredType(H5T_NATIVE_SCHAR);
    native.attr("unsignedChar") = PredType(H5T_NATIVE_UCHAR);
    native.attr("short") = PredType(H5T_NATIVE_SHORT);
    native.attr("unsignedShort") = PredType(H5T_NATIVE_USHORT);
    native.attr("int") = PredType(H5T_NATIVE_INT);
    native.attr("unsignedInt") = PredType(H5T_NATIVE_UINT);
    native.attr("long") = PredType(H5T_NATIVE_LONG);
    native.attr("unsignedLong") = PredType(H5T_NATIVE_ULONG);
    native.attr("longlong") = PredType(H5T_NATIVE_LLONG);
    native.attr("unsignedLongLong") = PredType(H5T_NATIVE_ULLONG);
    native.attr("bit8") = PredType(H5T_NATIVE_B8);
    native.attr("bit16") = PredType(H5T_NATIVE_B16);
    native.attr("bit32") = PredType(H5T_NATIVE_B32);
    native.attr("bit64") = PredType(H5T_NATIVE_B64);
    native.attr("hsize") = PredType(H5T_NATIVE_HSIZE);
    native.attr("hssize") = PredType(H5T_NATIVE_HSSIZE);
    native.attr("herr") = PredType(H5T_NATIVE_HERR);
    native.attr("bool") = PredType(H5T_NATIVE_HBOOL);

    native.attr("int8") = PredType(H5T_NATIVE_INT8);
    native.attr("uint8") = PredType(H5T_NATIVE_UINT8);
    native.attr("int16") = PredType(H5T_NATIVE_INT16);
    native.attr("uint16") = PredType(H5T_NATIVE_UINT16);
    native.attr("int32") = PredType(H5T_NATIVE_INT32);
    native.attr("uint32") = PredType(H5T_NATIVE_UINT32);
    native.attr("int64") = PredType(H5T_NATIVE_INT64);
    native.attr("uint64") = PredType(H5T_NATIVE_UINT64);

    native.attr("intLeast8") = PredType(H5T_NATIVE_INT_LEAST8);
    native.attr("uintLeast8") = PredType(H5T_NATIVE_UINT_LEAST8);
    native.attr("intLeast16") = PredType(H5T_NATIVE_INT_LEAST16);
    native.attr("uintLeast16") = PredType(H5T_NATIVE_UINT_LEAST16);
    native.attr("intLeast32") = PredType(H5T_NATIVE_INT_LEAST32);
    native.attr("uintLeast32") = PredType(H5T_NATIVE_UINT_LEAST32);
    native.attr("intLeast64") = PredType(H5T_NATIVE_INT_LEAST64);
    native.attr("uintLeast64") = PredType(H5T_NATIVE_UINT_LEAST64);

    native.attr("intFast8") = PredType(H5T_NATIVE_INT_FAST8);
    native.attr("uintFast8") = PredType(H5T_NATIVE_UINT_FAST8);
    native.attr("intFast16") = PredType(H5T_NATIVE_INT_FAST16);
    native.attr("uintFast16") = PredType(H5T_NATIVE_UINT_FAST16);
    native.attr("intFast32") = PredType(H5T_NATIVE_INT_FAST32);
    native.attr("uintFast32") = PredType(H5T_NATIVE_UINT_FAST32);
    native.attr("intFast64") = PredType(H5T_NATIVE_INT_FAST64);
    native.attr("uintFast64") = PredType(H5T_NATIVE_UINT_FAST64);

    // floating point
    native.attr("float") = PredType(H5T_NATIVE_FLOAT);
    native.attr("double") = PredType(H5T_NATIVE_DOUBLE);
    native.attr("longDouble") = PredType(H5T_NATIVE_LDOUBLE);

    // build a compound type to represent {std::complex<halffloat>}
    // make a new floating point type based on float
    auto nh = FloatType(PredType(H5T_NATIVE_FLOAT));
    // narrow it
    nh.setFields(15, 10, 5, 0, 10);
    nh.setBytes(2);
    // save it
    native.attr("half") = nh;
    // allocate the complex type
    auto ch = CompType(2 * nh.bytes());
    // insert the real and imaginary parts
    ch.insert("r", 0, nh);
    ch.insert("i", nh.bytes(), nh);
    // and attach it to the module
    native.attr("complexHalf") = ch;

    // build a compound type to represent complex types
    native.attr("complexFloat") = pyre::h5::datatype<std::complex<float>>();
    native.attr("complexDouble") = pyre::h5::datatype<std::complex<double>>();
    native.attr("complexUInt8") = pyre::h5::datatype<std::complex<std::uint8_t>>();
    native.attr("complexUInt16") = pyre::h5::datatype<std::complex<std::uint16_t>>();
    native.attr("complexUInt32") = pyre::h5::datatype<std::complex<std::uint32_t>>();
    native.attr("complexUInt64") = pyre::h5::datatype<std::complex<std::uint64_t>>();
    native.attr("complexInt8") = pyre::h5::datatype<std::complex<std::int8_t>>();
    native.attr("complexInt16") = pyre::h5::datatype<std::complex<std::int16_t>>();
    native.attr("complexInt32") = pyre::h5::datatype<std::complex<std::int32_t>>();
    native.attr("complexInt64") = pyre::h5::datatype<std::complex<std::int64_t>>();

    // all done
    return;
}


// end of file
