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
pyre::h5::py::datatypes::array(py::module & m)
{
    // add the class
    auto arrayType = py::class_<ArrayType, DataType>(
        // in scope
        m,
        // class name
        "ArrayType",
        // docstring
        "an HDF5 array datatype");

    // constructor
    arrayType.def(
        // the implementation
        py::init([](const DataType & type, const shape_t & shape) {
            return new ArrayType(type, shape.size(), &shape[0]);
        }),
        // the signature
        "type"_a, "shape"_a,
        // the docstring
        "build an array of the given {type} and {shape}");

    // all done
    return;
}


// end of file
