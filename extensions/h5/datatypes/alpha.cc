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


// encapsulations of the alpha datatypes
void
pyre::h5::py::datatypes::alpha(py::module & m)
{
    // make a new namespace to hold alpha datatype descriptions
    auto alpha = m.def_submodule(
        // the name of the module
        "alpha",
        // its docstring
        "a collection of alpha types");

    // integral
    alpha.attr("int8") = H5::PredType::ALPHA_I8;
    alpha.attr("int16") = H5::PredType::ALPHA_I16;
    alpha.attr("int32") = H5::PredType::ALPHA_I32;
    alpha.attr("int64") = H5::PredType::ALPHA_I64;

    alpha.attr("uint8") = H5::PredType::ALPHA_U8;
    alpha.attr("uint16") = H5::PredType::ALPHA_U16;
    alpha.attr("uint32") = H5::PredType::ALPHA_U32;
    alpha.attr("uint64") = H5::PredType::ALPHA_U64;

    alpha.attr("b8") = H5::PredType::ALPHA_B8;
    alpha.attr("b16") = H5::PredType::ALPHA_B16;
    alpha.attr("b32") = H5::PredType::ALPHA_B32;
    alpha.attr("b64") = H5::PredType::ALPHA_B64;

    // floating point
    alpha.attr("f32") = H5::PredType::ALPHA_F32;
    alpha.attr("f64") = H5::PredType::ALPHA_F64;

    // all done
    return;
}


// end of file
