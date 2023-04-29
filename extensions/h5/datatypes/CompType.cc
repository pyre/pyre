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
pyre::h5::py::datatypes::compound(py::module & m)
{
    // add the class
    auto cls = py::class_<CompType, DataType>(
        // in scope
        m,
        // class name
        "CompType",
        // docstring
        "an HDF5 compound datatype");

    // constructors
    cls.def(
        // the implementation
        py::init<std::size_t>(),
        // the signature
        "size"_a,
        // the docstring
        "make a compound type of the give {size} in bytes");

    // my length is the number of members
    cls.def_property_readonly(
        // the name
        "members",
        // the implementation
        &CompType::getNmembers,
        // the docstring
        "the number of members in this compound type");

    cls.def_property(
        // the name
        "bytes",
        // the getter
        &CompType::getSize,
        // the setter
        &CompType::setSize,
        // the docstring
        "get/set the overall size");

    // member layout
    cls.def(
        // the name
        "index",
        // the implementation
        [](const CompType & self, const string_t & name) -> int {
            // easy enough
            return self.getMemberIndex(name);
        },
        // the signature
        "name"_a,
        // the docstring
        "return the index of the member by the given {name}");

    cls.def(
        // the name
        "name",
        // the implementation
        &CompType::getMemberName,
        // the signature
        "index"_a,
        // the docstring
        "return the name of the member at the given {index}");

    cls.def(
        // the name
        "offset",
        // the implementation
        &CompType::getMemberOffset,
        // the signature
        "index"_a,
        // the docstring
        "return the offset of the member at the given {index}");

    cls.def(
        // the name
        "type",
        // the implementation
        [](const CompType & self, unsigned int index) -> DataType * {
            // get the type class of the member
            auto cls = self.getMemberClass(index);
            // deduce
            switch (cls) {
                // integers
                case H5T_INTEGER:
                    // return the integer data type descriptor
                    return new H5::IntType(self.getMemberIntType(index));
                // floats
                case H5T_FLOAT:
                    // return the float data type descriptor
                    return new H5::FloatType(self.getMemberFloatType(index));
                // strings
                case H5T_STRING:
                    // return the string data type descriptor
                    return new H5::StrType(self.getMemberStrType(index));
                // compound types
                case H5T_COMPOUND:
                    // return the compound data type descriptor
                    return new H5::CompType(self.getMemberCompType(index));
                // enum types
                case H5T_ENUM:
                    // return the enum data type descriptor
                    return new H5::EnumType(self.getMemberEnumType(index));
                // variable length types
                case H5T_VLEN:
                    // return the variable length data type descriptor
                    return new H5::VarLenType(self.getMemberVarLenType(index));
                // array types
                case H5T_ARRAY:
                    // return the array data type descriptor
                    return new H5::ArrayType(self.getMemberArrayType(index));
                // by default
                default:
                    // grab whatever generic information is available
                    return new H5::DataType(self.getMemberDataType(index));
            }
            // this should be unreachable, but just in case new paths open up
            return new H5::DataType(self.getMemberDataType(index));
        },
        // the signature
        "index"_a,
        // the docstring
        "deduce the type of the member at the given {index}");

    // interface
    cls.def(
        // the name
        "insert",
        // the implementation
        &CompType::insertMember,
        // the signature
        "name"_a, "offset"_a, "type"_a,
        // the docstring
        "insert {name} of {type} at the given {offset}");

    cls.def(
        // the name
        "pack",
        // the implementation
        &CompType::pack,
        // the docstring
        "recursively remove padding from within this compound type");

    // all done
    return;
}


// end of file
