// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file objects
void
pyre::h5::py::datatypes::predefined(py::module & m)
{
    // add the class
    auto predType = py::class_<PredType, DataType>(
        // in scope
        m,
        // class name
        "PredType",
        // docstring
        "an HDF5 predefined datatype");

    // all done
    return;
}


// end of file
