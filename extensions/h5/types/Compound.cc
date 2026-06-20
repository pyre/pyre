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
pyre::h5::py::types::compound(py::module & m)
{
    // add the class
    auto cls = py::class_<CompType, DataType>(
        // in scope
        m,
        // class name
        "compound",
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
        &CompType::members,
        // the docstring
        "the number of members in this compound type");

    // my names of the group members
    cls.def_property_readonly(
        // the name
        "names",
        // the implementation
        [](const CompType & self) -> names_t {
            // get the number of members
            auto members = self.members();
            // make a pile
            auto names = names_t(members);
            // go through the known members
            for (int idx = 0; idx < members; ++idx) {
                // get the name of each one and put it in the pile
                names[idx] = self.memberName(idx);
            }
            // all done
            return names;
        },
        // the docstring
        "the names of the members of this compound type");


    cls.def_property(
        // the name
        "bytes",
        // the getter
        &CompType::bytes,
        // the setter
        &CompType::setBytes,
        // the docstring
        "get/set the overall size");

    // member layout
    cls.def(
        // the name
        "index",
        // the implementation
        [](const CompType & self, const string_t & name) -> int {
            // easy enough
            return self.memberIndex(name);
        },
        // the signature
        "name"_a,
        // the docstring
        "return the index of the member by the given {name}");

    cls.def(
        // the name
        "name",
        // the implementation
        &CompType::memberName,
        // the signature
        "index"_a,
        // the docstring
        "return the name of the member at the given {index}");

    cls.def(
        // the name
        "offset",
        // the implementation
        &CompType::memberOffset,
        // the signature
        "index"_a,
        // the docstring
        "return the offset of the member at the given {index}");

    cls.def(
        // the name
        "type",
        // the implementation
        [](const CompType & self, unsigned int index) -> DataType * {
            // {memberType} hands back a fresh handle the new wrapper adopts
            auto id = self.memberType(index);
            // deduce its class
            switch (self.memberClass(index)) {
                // integers
                case H5T_INTEGER:
                    // return the integer data type descriptor
                    return new IntType(id);
                // floats
                case H5T_FLOAT:
                    // return the float data type descriptor
                    return new FloatType(id);
                // strings
                case H5T_STRING:
                    // return the string data type descriptor
                    return new StrType(id);
                // compound types
                case H5T_COMPOUND:
                    // return the compound data type descriptor
                    return new CompType(id);
                // enum types
                case H5T_ENUM:
                    // return the enum data type descriptor
                    return new EnumType(id);
                // variable length types
                case H5T_VLEN:
                    // return the variable length data type descriptor
                    return new VarLenType(id);
                // array types
                case H5T_ARRAY:
                    // return the array data type descriptor
                    return new ArrayType(id);
                // by default
                default:
                    // grab whatever generic information is available
                    return new DataType(id);
            }
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
        &CompType::insert,
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
