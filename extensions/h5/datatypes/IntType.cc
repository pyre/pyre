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
pyre::h5::py::datatypes::int_(py::module & m)
{
    // add the class
    auto intType = py::class_<IntType, AtomType>(
        // in scope
        m,
        // class name
        "IntType",
        // docstring
        "an HDF5 int datatype");

    // constructor
    intType.def(py::init<>());

    // all done
    return;
}


// end of file
