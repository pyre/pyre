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
pyre::h5::py::types::arrayClass(py::module & m)
{
    // register the class
    py::class_<ArrayType, DataType>(
        // in scope
        m,
        // class name
        "array",
        // docstring
        "an HDF5 array datatype");

    // all done
    return;
}


// bind the array datatypes
void
pyre::h5::py::types::array()
{
    // the class, registered by {arrayClass}
    auto arrayType = py::class_<ArrayType, DataType>(py::type::of<ArrayType>());

    // constructor
    arrayType.def(
        // the implementation
        py::init(
            [](const DataType & type, const shape_t & shape) { return ArrayType(type, shape); }),
        // the signature
        "type"_a, "shape"_a,
        // the docstring
        "build an array of the given {type} and {shape}");

    // all done
    return;
}


// end of file
