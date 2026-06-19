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


// encapsulations of the intel datatypes
void
pyre::h5::py::datatypes::intel(py::module & m)
{
    // make a new namespace to hold intel datatype descriptions
    auto intel = m.def_submodule(
        // the name of the module
        "intel",
        // its docstring
        "a collection of intel types");

    // integral
    intel.attr("int8") = PredType(H5T_INTEL_I8);
    intel.attr("int16") = PredType(H5T_INTEL_I16);
    intel.attr("int32") = PredType(H5T_INTEL_I32);
    intel.attr("int64") = PredType(H5T_INTEL_I64);

    intel.attr("uint8") = PredType(H5T_INTEL_U8);
    intel.attr("uint16") = PredType(H5T_INTEL_U16);
    intel.attr("uint32") = PredType(H5T_INTEL_U32);
    intel.attr("uint64") = PredType(H5T_INTEL_U64);

    intel.attr("b8") = PredType(H5T_INTEL_B8);
    intel.attr("b16") = PredType(H5T_INTEL_B16);
    intel.attr("b32") = PredType(H5T_INTEL_B32);
    intel.attr("b64") = PredType(H5T_INTEL_B64);

    // floating point
    intel.attr("f32") = PredType(H5T_INTEL_F32);
    intel.attr("f64") = PredType(H5T_INTEL_F64);

    // all done
    return;
}


// end of file
