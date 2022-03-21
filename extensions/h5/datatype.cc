// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file objects
void
h5::py::datatype(py::module & m)
{
    // add bindings for hdf5 datatypes
    auto datatype = py::class_<DataType>(
        // in scope
        m,
        // class name
        "DataType",
        // docstring
        "an HDF5 datatype");

    auto pred = py::class_<PredType, DataType>(
        // in scope
        m,
        // class name
        "PredType",
        // docstring
        "an HDF5 predefined datatype");

    // make a new namespace to hold builtin datatype descriptions
    auto datatypes = m.def_submodule(
        // the name of the module
        "datatypes",
        // its docstring
        "a collection of predefined types");

    // make a new namespace to hold native datatype descriptions
    auto native = datatypes.def_submodule(
        // the name of the module
        "native",
        // its docstring
        "a collection of native types");

    // add the datatypes
    native.attr("char") = H5::PredType::NATIVE_CHAR;
    native.attr("unsigned_char") = H5::PredType::NATIVE_UCHAR;
    native.attr("short") = H5::PredType::NATIVE_SHORT;
    native.attr("unsigned_short") = H5::PredType::NATIVE_USHORT;
    native.attr("int") = H5::PredType::NATIVE_INT;
    native.attr("unsigned_int") = H5::PredType::NATIVE_UINT;
    native.attr("long") = H5::PredType::NATIVE_LONG;
    native.attr("unsigned_long") = H5::PredType::NATIVE_ULONG;
    native.attr("float") = H5::PredType::NATIVE_FLOAT;
    native.attr("double") = H5::PredType::NATIVE_DOUBLE;

    // all done
    return;
}


// end of file
