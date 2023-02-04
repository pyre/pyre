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
pyre::h5::py::datatypes::float_(py::module & m)
{
    // add the class
    auto floatType = py::class_<FloatType, AtomType>(
        // in scope
        m,
        // class name
        "FloatType",
        // docstring
        "an HDF5 float datatype");

    // constructor
    floatType.def(py::init<>());

    // all done
    return;
}


// end of file
