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


// file objects
void
pyre::h5::py::types::varlen(py::module & m)
{
    // add the class
    auto varlenType = py::class_<VarLenType, DataType>(
        // in scope
        m,
        // class name
        "varlen",
        // docstring
        "an HDF5 variable length datatype");

    // all done
    return;
}


// end of file
