// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


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
    // from an existing type
    cls.def(
        // the implementation
        py::init<hid_t>(),
        // the signature
        "id"_a,
        // the docstring
        "make a type using the id of an existing one");

    // from a predefined type
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
            // i am a named datatype
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

    // retrieve the base type of a type
    cls.def_property_readonly(
        // the name
        "super",
        // the implementation
        &DataType::getSuper,
        // the docstring
        "retrieve the base type from which this one is derived");

    // check whether this datatype is a certain type of datatype
    cls.def(
        // the name
        "isA",
        // the implementation
        py::overload_cast<H5T_class_t>(&DataType::detectClass, py::const_),
        // the signature
        "type"_a,
        // the docsting
        "check whether this data type is of a given type");

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

    // access to the datatype attributes
    attributes(cls);

    // all done
    return;
}


// end of file
