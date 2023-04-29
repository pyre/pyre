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
pyre::h5::py::datatypes::enum_(py::module & m)
{
    // add the class
    auto enumType = py::class_<EnumType, DataType>(
        // in scope
        m,
        // class name
        "EnumType",
        // docstring
        "an HDF5 array datatype");

    // constructor
    enumType.def(py::init<>());

    // all done
    return;
}


// end of file
