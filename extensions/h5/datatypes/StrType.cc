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
    auto cls = py::class_<StrType, AtomType>(
        // in scope
        m,
        // class name
        "StrType",
        // docstring
        "an HDF5 string datatype");

    // constructors
    // default
    cls.def(py::init<>());
    // from a predefined float type
    cls.def(py::init<const PredType &>());

    // properties
    cls.def_property(
        // the name
        "charset",
        // the getter
        &StrType::getCset,
        // the setter
        &StrType::setCset,
        // the docstring
        "get/set the string character set");

    cls.def_property(
        // the name
        "strpad",
        // the getter
        &StrType::getStrpad,
        // the setter
        &StrType::setStrpad,
        // the docstring
        "get/set the string padding method");

    // all done
    return;
}


// end of file
