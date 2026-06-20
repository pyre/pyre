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


// encapsulations of the little endian datatypes
void
pyre::h5::py::types::little(py::module & m)
{
    // make a new namespace to hold little endian datatype descriptions
    auto little = m.def_submodule(
        // the name of the module
        "little",
        // its docstring
        "a collection of little endian types");

    // add a selection of datatypes
    little.attr("int8") = PredType(H5T_STD_I8LE);
    little.attr("uint8") = PredType(H5T_STD_U8LE);
    little.attr("int16") = PredType(H5T_STD_I16LE);
    little.attr("uint16") = PredType(H5T_STD_U16LE);
    little.attr("int32") = PredType(H5T_STD_I32LE);
    little.attr("uint32") = PredType(H5T_STD_U32LE);
    little.attr("int64") = PredType(H5T_STD_I64LE);
    little.attr("uint64") = PredType(H5T_STD_U64LE);

    // all done
    return;
}


// end of file
