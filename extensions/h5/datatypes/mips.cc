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


// encapsulations of the mips datatypes
void
pyre::h5::py::datatypes::mips(py::module & m)
{
    // make a new namespace to hold mips datatype descriptions
    auto mips = m.def_submodule(
        // the name of the module
        "mips",
        // its docstring
        "a collection of mips types");

    // integral
    mips.attr("int8") = H5::PredType::MIPS_I8;
    mips.attr("int16") = H5::PredType::MIPS_I16;
    mips.attr("int32") = H5::PredType::MIPS_I32;
    mips.attr("int64") = H5::PredType::MIPS_I64;

    mips.attr("uint8") = H5::PredType::MIPS_U8;
    mips.attr("uint16") = H5::PredType::MIPS_U16;
    mips.attr("uint32") = H5::PredType::MIPS_U32;
    mips.attr("uint64") = H5::PredType::MIPS_U64;

    mips.attr("b8") = H5::PredType::MIPS_B8;
    mips.attr("b16") = H5::PredType::MIPS_B16;
    mips.attr("b32") = H5::PredType::MIPS_B32;
    mips.attr("b64") = H5::PredType::MIPS_B64;

    // floating point
    mips.attr("f32") = H5::PredType::MIPS_F32;
    mips.attr("f64") = H5::PredType::MIPS_F64;

    // all done
    return;
}


// end of file
