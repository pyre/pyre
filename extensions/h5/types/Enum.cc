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
pyre::h5::py::types::enum_(py::module & m)
{
    // add the class
    auto enumType = py::class_<EnumType, DataType>(
        // in scope
        m,
        // class name
        "enum",
        // docstring
        "an HDF5 enum datatype");

    // constructors
    enumType.def(py::init<>());

    // from an existing type
    enumType.def(
        // the implementation
        py::init([](hid_t id) {
            // {id} belongs to someone else; take out a reference of my own, then adopt it
            H5Iinc_ref(id);
            return EnumType(id);
        }),
        // the signature
        "id"_a,
        // the docstring
        "make an enum type using the id of an existing one");

    // the number of members
    enumType.def_property_readonly(
        // the name
        "members",
        // the implementation
        &EnumType::members,
        // the docstring
        "the number of members in this enum type");

    // interface
    enumType.def(
        // the name
        "name",
        // the implementation
        [](const EnumType & self, unsigned int index) -> string_t {
            // look up the value at {index}, then map it back to its name
            return self.nameOf(self.memberValue(index));
        },
        // the signature
        "index"_a,
        // the docstring
        "the name of the member at position {index} in the type description");

    enumType.def(
        // the name
        "value",
        // the implementation
        &EnumType::memberValue,
        // the signature
        "index"_a,
        // the docstring
        "the value of the member at position {index} in the type description");

    enumType.def(
        // the name
        "map",
        // the implementation
        [](const EnumType & self) -> kv_t<long> {
            // build the table
            auto map = kv_t<long>();
            // go through the members
            for (unsigned int m = 0; m < static_cast<unsigned int>(self.members()); ++m) {
                // get the value of this member
                auto value = self.memberValue(m);
                // map it back to its name
                auto key = self.nameOf(value);
                // add the pair to the pile
                map.emplace(key, value);
            }
            // return the map
            return map;
        },
        // the docstring
        "generate my (name, value) map");

    // all done
    return;
}


// end of file
