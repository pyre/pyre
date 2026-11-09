// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package global declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// register the class, so that every signature can name it
void
pyre::h5::py::types::strClass(py::module & m)
{
    // register the class
    py::class_<StrType, AtomType>(
        // in scope
        m,
        // class name
        "str",
        // docstring
        "an HDF5 string datatype");

    // all done
    return;
}


// bind the string datatypes
void
pyre::h5::py::types::str()
{
    // the class, registered by {strClass}
    auto cls = py::class_<StrType, AtomType>(py::type::of<StrType>());

    // constructors
    // from an existing type
    cls.def(
        // the implementation
        py::init([](hid_t id) {
            // {id} belongs to someone else; take out a reference of my own, then adopt it
            H5Iinc_ref(id);
            return StrType(id);
        }),
        // the signature
        "id"_a,
        // the docstring
        "make a string type using the id of an existing one");

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
        &StrType::charset,
        // the setter
        pyre::py::setter(cls, &StrType::setCset),
        // the docstring
        "get/set the string character set");

    cls.def_property(
        // the name
        "strpad",
        // the getter
        &StrType::strpad,
        // the setter
        pyre::py::setter(cls, &StrType::setStrpad),
        // the docstring
        "get/set the string padding method");

    // all done
    return;
}


// end of file
