// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


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
    native.attr("char") = H5::PredType::NATIVE_CHAR;
    native.attr("signedChar") = H5::PredType::NATIVE_SCHAR;
    native.attr("unsignedChar") = H5::PredType::NATIVE_UCHAR;
    native.attr("short") = H5::PredType::NATIVE_SHORT;
    native.attr("unsignedShort") = H5::PredType::NATIVE_USHORT;
    native.attr("int") = H5::PredType::NATIVE_INT;
    native.attr("unsignedInt") = H5::PredType::NATIVE_UINT;
    native.attr("long") = H5::PredType::NATIVE_LONG;
    native.attr("unsignedLong") = H5::PredType::NATIVE_ULONG;
    native.attr("longlong") = H5::PredType::NATIVE_LLONG;
    native.attr("unsignedLongLong") = H5::PredType::NATIVE_ULLONG;
    native.attr("bit8") = H5::PredType::NATIVE_B8;
    native.attr("bit16") = H5::PredType::NATIVE_B16;
    native.attr("bit32") = H5::PredType::NATIVE_B32;
    native.attr("bit64") = H5::PredType::NATIVE_B64;
    native.attr("hsize") = H5::PredType::NATIVE_HSIZE;
    native.attr("hssize") = H5::PredType::NATIVE_HSSIZE;
    native.attr("herr") = H5::PredType::NATIVE_HERR;
    native.attr("bool") = H5::PredType::NATIVE_HBOOL;

    native.attr("int8") = H5::PredType::NATIVE_INT8;
    native.attr("uint8") = H5::PredType::NATIVE_UINT8;
    native.attr("int16") = H5::PredType::NATIVE_INT16;
    native.attr("uint16") = H5::PredType::NATIVE_UINT16;
    native.attr("int32") = H5::PredType::NATIVE_INT32;
    native.attr("uint32") = H5::PredType::NATIVE_UINT32;
    native.attr("int64") = H5::PredType::NATIVE_INT64;
    native.attr("uint64") = H5::PredType::NATIVE_UINT64;

    native.attr("intLeast8") = H5::PredType::NATIVE_INT_LEAST8;
    native.attr("uintLeast8") = H5::PredType::NATIVE_UINT_LEAST8;
    native.attr("intLeast16") = H5::PredType::NATIVE_INT_LEAST16;
    native.attr("uintLeast16") = H5::PredType::NATIVE_UINT_LEAST16;
    native.attr("intLeast32") = H5::PredType::NATIVE_INT_LEAST32;
    native.attr("uintLeast32") = H5::PredType::NATIVE_UINT_LEAST32;
    native.attr("intLeast64") = H5::PredType::NATIVE_INT_LEAST64;
    native.attr("uintLeast64") = H5::PredType::NATIVE_UINT_LEAST64;

    native.attr("intFast8") = H5::PredType::NATIVE_INT_FAST8;
    native.attr("uintFast8") = H5::PredType::NATIVE_UINT_FAST8;
    native.attr("intFast16") = H5::PredType::NATIVE_INT_FAST16;
    native.attr("uintFast16") = H5::PredType::NATIVE_UINT_FAST16;
    native.attr("intFast32") = H5::PredType::NATIVE_INT_FAST32;
    native.attr("uintFast32") = H5::PredType::NATIVE_UINT_FAST32;
    native.attr("intFast64") = H5::PredType::NATIVE_INT_FAST64;
    native.attr("uintFast64") = H5::PredType::NATIVE_UINT_FAST64;

    // floating point
    native.attr("float") = H5::PredType::NATIVE_FLOAT;
    native.attr("double") = H5::PredType::NATIVE_DOUBLE;
    native.attr("longDouble") = H5::PredType::NATIVE_LDOUBLE;

    // build a compound type to represent {std::complex<halffloat>}
    // make a new floating point type based on float
    auto nh = H5::FloatType(H5::PredType::NATIVE_FLOAT);
    // narrow it
    nh.setFields(15, 10, 5, 0, 10);
    nh.setSize(2);
    // save it
    native.attr("half") = nh;
    // allocate the complex type
    auto ch = H5::CompType(2 * nh.getSize());
    // insert the real and imaginary parts
    ch.insertMember("r", 0, nh);
    ch.insertMember("i", nh.getSize(), nh);
    // and attach it to the module
    native.attr("complexHalf") = ch;

    // build a compound type to represent {std::complex<float>}
    // grab the native float
    auto nf = H5::PredType::NATIVE_FLOAT;
    // allocate the complex type
    auto cf = H5::CompType(2 * nf.getSize());
    // insert the real and imaginary parts
    cf.insertMember("r", 0, nf);
    cf.insertMember("i", nf.getSize(), nf);
    // and attach it to the module
    native.attr("complexFloat") = cf;

    // build a compound type to represent {std::complex<double>}
    // grab the native double
    auto nd = H5::PredType::NATIVE_DOUBLE;
    // allocate the complex type
    auto cd = H5::CompType(2 * nd.getSize());
    // insert the real and imaginary parts
    cd.insertMember("r", 0, nd);
    cd.insertMember("i", nd.getSize(), nd);
    // and attach it
    native.attr("complexDouble") = cd;

    // all done
    return;
}


// end of file
