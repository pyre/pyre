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
pyre::h5::py::datatypes::int_(py::module & m)
{
    // add the class
    auto cls = py::class_<IntType, AtomType>(
        // in scope
        m,
        // class name
        "IntType",
        // docstring
        "an HDF5 int datatype");

    // constructors
    // from an existing type
    cls.def(
        // the implementation
        py::init<hid_t>(),
        // the signature
        "id"_a,
        // the docstring
        "make an integer type using the id of an existing one");

    // from a predefined integer type
    cls.def(
        // the implementation
        py::init<const PredType &>(),
        // the signature
        "type"_a,
        // the docstring
        "make a copy of the predefined {type}");

    // properties
    cls.def_property(
        // the name
        "sign",
        // the getter
        &IntType::getSign,
        // the setter
        &IntType::setSign,
        // the docstring
        "get/set the sign type");

    // all done
    return;
}


// end of file
