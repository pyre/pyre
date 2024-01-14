// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


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
        "an HDF5 enum datatype");

    // constructor
    enumType.def(py::init<>());

    // the number of members
    enumType.def_property_readonly(
        // the name
        "members",
        // the implementation
        &EnumType::getNmembers,
        // the docstring
        "the number of members in this enum type");

    // all done
    return;
}


// end of file
