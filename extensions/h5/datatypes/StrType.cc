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
pyre::h5::py::datatypes::str(py::module & m)
{
    // add the class
    auto strType = py::class_<StrType, AtomType>(
        // in scope
        m,
        // class name
        "StrType",
        // docstring
        "an HDF5 string datatype");

    // constructor
    strType.def(py::init<>());

    // all done
    return;
}


// end of file
