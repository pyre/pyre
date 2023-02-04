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
pyre::h5::py::datatypes::datatype(py::module & m)
{
    // add bindings for the base hdf5 datatype
    auto dataType = py::class_<DataType>(
        // in scope
        m,
        // class name
        "DataType",
        // docstring
        "the base HDF5 datatype");

    // constructor
    dataType.def(py::init<>());

    // the name of the type
    dataType.def_property_readonly(
        // the name
        "name",
        // the implementation
        &DataType::fromClass,
        // the docstring
        "the name of this datatype");

    // all done
    return;
}


// end of file