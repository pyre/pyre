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


// encapsulations of the big endian datatypes
void
pyre::h5::py::datatypes::big(py::module & m)
{
    // make a new namespace to hold big endian datatype descriptions
    auto big = m.def_submodule(
        // the name of the module
        "big",
        // its docstring
        "a collection of big endian types");

    // add a selection of datatypes
    big.attr("int8") = H5::PredType::STD_I8BE;
    big.attr("uint8") = H5::PredType::STD_U8BE;
    big.attr("int16") = H5::PredType::STD_I16BE;
    big.attr("uint16") = H5::PredType::STD_U16BE;
    big.attr("int32") = H5::PredType::STD_I32BE;
    big.attr("uint32") = H5::PredType::STD_U32BE;
    big.attr("int64") = H5::PredType::STD_I64BE;
    big.attr("uint64") = H5::PredType::STD_U64BE;

    // all done
    return;
}


// end of file
