// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
pyre::h5::py::types::datatype(py::module & m)
{
    // add bindings for the base hdf5 datatype
    auto cls = py::class_<DataType>(
        // in scope
        m,
        // class name
        "datatype",
        // docstring
        "the base HDF5 datatype");

    // constructor
    // from an existing type
    cls.def(
        // the implementation
        py::init([](hid_t id) {
            // {id} belongs to someone else; take out a reference of my own so my bookkeeping
            // stays balanced, then adopt it
            H5Iinc_ref(id);
            return DataType(id);
        }),
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
        &DataType::className,
        // the docstring
        "the name of this datatype");

    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &DataType::id,
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
        &DataType::cell,
        // the docstring
        "get my class type");

    // get the size of the data type
    cls.def_property_readonly(
        // the name
        "bytes",
        // the implementation
        &DataType::bytes,
        // the docstring
        "retrieve the size of this data type");

    // retrieve the base type of a type
    cls.def_property_readonly(
        // the name
        "super",
        // the implementation
        &DataType::super,
        // the docstring
        "retrieve the base type from which this one is derived");

    // check whether this datatype is a certain type of datatype
    cls.def(
        // the name
        "isA",
        // the implementation
        &DataType::isA,
        // the signature
        "type"_a,
        // the docsting
        "check whether this data type is of a given type");

    // interface
    cls.def(
        // the name
        "close",
        // the implementation
        &DataType::close,
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
        &DataType::decode,
        // the signature
        "buffer"_a,
        // the docstring
        "reconstruct a type from its binary object description");

    // datatype equality and inequality, via {H5Tequal}
    cls.def(
        // the implementation
        py::self == py::self,
        // the docstring
        "whether i describe the same datatype as another");
    cls.def(
        // the implementation
        py::self != py::self,
        // the docstring
        "whether i describe a different datatype than another");

    // access to the attributes of a named (committed) datatype, now that {Datatype} derives from
    // {Location}
    attributes(cls);

    // all done
    return;
}


// end of file
