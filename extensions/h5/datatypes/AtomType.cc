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


// file objects
void
pyre::h5::py::datatypes::atom(py::module & m)
{
    // add the class
    auto atomType = py::class_<AtomType, DataType>(
        // in scope
        m,
        // class name
        "AtomType",
        // docstring
        "an HDF5 atom datatype");

    // all done
    return;
}


// end of file
