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
    // from a predefined float type
    cls.def(
        // the implementation
        py::init<const PredType &>(),
        // the signature
        "type"_a,
        // the docstring
        "make a copy of the predefined {type}");

    // the name of the type
    cls.def_property_readonly(
        // the name
        "className",
        // the implementation
        &DataType::fromClass,
        // the docstring
        "the name of this datatype");

    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &DataType::getId,
        // the docstring
        "the h5 handle of this datatype");

    // the object categories
    cls.def_property_readonly_static(
        // the name
        "identifierType",
        // the implementation
        [](const py::object &) -> H5I_type_t {
            // i am a group
            return H5I_DATATYPE;
        },
        // the docstring
        "get my h5 identifier type");

    cls.def_property_readonly_static(
        // the name
        "objectType",
        // the implementation
        [](const py::object &) -> H5O_type_t {
            // i am a group
            return H5O_TYPE_NAMED_DATATYPE;
        },
        // the docstring
        "get my h5 object type");

    // the class type, an {H5T_class_t}
    cls.def_property_readonly(
        // the name
        "cell",
        // the implementation
        &DataType::getClass,
        // the docstring
        "get my class type");

    // get the size of the data type
    cls.def_property_readonly(
        // the name
        "bytes",
        // the implementation
        &DataType::getSize,
        // the docstring
        "retrieve the size of this data type");

    // interface
    cls.def(
        // the name
        "close",
        // the implementation
        [](DataType & self) -> void {
            // invoke the virtual function
            self.close();
            // all done
            return;
        },
        // the docstring
        "close the associated h5 handle");

    cls.def(
        // the name
        "encode",
        // the implementation
        &DataType::encode,
        // the docstring
        "create a binary object description");

    cls.def(
        // the name
        "decode",
        // the implementation
        [](const DataType & self) -> DataType * {
            // invoke the virtual function
            return self.decode();
        },
        // the docstring
        "decode the binary object description");

    // all done
    return;
}


// end of file
