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
    // from a specific predefined type
    cls.def(
        // the implementation
        py::init<const PredType &>(),
        // the signature
        "type"_a,
        // the docstrings
        "make a string type with a specific {type} as its cell");

    // native string of a given size
    cls.def(
        // the implementation
        py::init([](size_t cells) { return StrType(0, cells); }),
        // the signature
        "cells"_a,
        // the docstring
        "make a native c-style string of the given number of {cells}");

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
