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


// encapsulations of the std datatypes
void
pyre::h5::py::datatypes::std(py::module & m)
{
    // make a new namespace to hold native datatype descriptions
    auto std = m.def_submodule(
        // the name of the module
        "std",
        // its docstring
        "the standard data types");

    // add the standard datatypes
    std.attr("c_s1") = PredType(H5T_C_S1);
    std.attr("fortran_s1") = PredType(H5T_FORTRAN_S1);

    std.attr("i8be") = PredType(H5T_STD_I8BE);
    std.attr("i8le") = PredType(H5T_STD_I8LE);
    std.attr("i16be") = PredType(H5T_STD_I16BE);
    std.attr("i16le") = PredType(H5T_STD_I16LE);
    std.attr("i32be") = PredType(H5T_STD_I32BE);
    std.attr("i32le") = PredType(H5T_STD_I32LE);
    std.attr("i64be") = PredType(H5T_STD_I64BE);
    std.attr("i64le") = PredType(H5T_STD_I64LE);

    std.attr("u8be") = PredType(H5T_STD_U8BE);
    std.attr("u8le") = PredType(H5T_STD_U8LE);
    std.attr("u16be") = PredType(H5T_STD_U16BE);
    std.attr("u16le") = PredType(H5T_STD_U16LE);
    std.attr("u32be") = PredType(H5T_STD_U32BE);
    std.attr("u32le") = PredType(H5T_STD_U32LE);
    std.attr("u64be") = PredType(H5T_STD_U64BE);
    std.attr("u64le") = PredType(H5T_STD_U64LE);

    std.attr("b8be") = PredType(H5T_STD_B8BE);
    std.attr("b8le") = PredType(H5T_STD_B8LE);
    std.attr("b16be") = PredType(H5T_STD_B16BE);
    std.attr("b16le") = PredType(H5T_STD_B16LE);
    std.attr("b32be") = PredType(H5T_STD_B32BE);
    std.attr("b32le") = PredType(H5T_STD_B32LE);
    std.attr("b64be") = PredType(H5T_STD_B64BE);
    std.attr("b64le") = PredType(H5T_STD_B64LE);

    // all done
    return;
}


// end of file
