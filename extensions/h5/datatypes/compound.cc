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
pyre::h5::py::datatypes::compound(py::module & m)
{
    // add the class
    auto compType = py::class_<CompType, DataType>(
        // in scope
        m,
        // class name
        "CompType",
        // docstring
        "an HDF5 compound datatype");

    // all done
    return;
}


// end of file
