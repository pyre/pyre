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
    auto cls = py::class_<DataType>(
        // in scope
        m,
        // class name
        "DataType",
        // docstring
        "the base HDF5 datatype");

    // constructor
    cls.def(py::init<>());

    // the name of the type
    cls.def_property_readonly(
        // the name
        "className",
        // the implementation
        &DataType::fromClass,
        // the docstring
        "the name of this datatype");

    // the class type, an {H5T_class_t}
    cls.def_property_readonly(
        // the name
        "cell",
        // the implementation
        &DataType::getClass,
        // the docstring
        "get my class type");

    // interface
    cls.def(
        // the name
        "close",
        // the implementation
        [](DataType & self) -> void {
            // invoked the virtual function
            self.close();
            // all done
            return;
        },
        // the docstring
        "close the associated h5 handle");

    // all done
    return;
}


// end of file
