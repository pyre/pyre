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


// encapsulations of the IEEE floating datatypes
void
pyre::h5::py::datatypes::ieee(py::module & m)
{
    // make a new namespace to hold native datatype descriptions
    auto ieee = m.def_submodule(
        // the name of the module
        "ieee",
        // its docstring
        "the IEEE floating point types");

    // IEEE floating point
    ieee.attr("f32be") = H5::PredType::IEEE_F32BE;
    ieee.attr("f32le") = H5::PredType::IEEE_F32LE;
    ieee.attr("f64be") = H5::PredType::IEEE_F64BE;
    ieee.attr("f64le") = H5::PredType::IEEE_F64LE;

    // all done
    return;
}


// end of file
