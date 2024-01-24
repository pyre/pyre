// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


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
pyre::h5::py::datatypes::enum_(py::module & m)
{
    // add the class
    auto enumType = py::class_<EnumType, DataType>(
        // in scope
        m,
        // class name
        "EnumType",
        // docstring
        "an HDF5 enum datatype");

    // constructor
    enumType.def(py::init<>());

    // the number of members
    enumType.def_property_readonly(
        // the name
        "members",
        // the implementation
        &EnumType::getNmembers,
        // the docstring
        "the number of members in this enum type");

    // interface
    enumType.def(
        // the name
        "name",
        // the implementation
        [](const EnumType & self, int index) -> string_t {
            // make some room for the value
            long value = 0;
            // retrieve it
            self.getMemberValue(index, &value);
            // and use it to get the name
            return self.nameOf(&value, 256);
        },
        // the signature
        "index"_a,
        // the docstring
        "the name of the member at position {index} in the type description");

    enumType.def(
        // the name
        "value",
        // the implementation
        [](const EnumType & self, int index) -> long {
            // make some room for the value
            long value = 0;
            // retrieve it
            self.getMemberValue(index, &value);
            // and return it
            return value;
        },
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
            for (int m = 0; m < self.getNmembers(); ++m) {
                // make some room for the value
                long value = 0;
                // retrieve it
                self.getMemberValue(m, &value);
                // and use it to get the name
                auto key = self.nameOf(&value, 256);
                // add the pair ot the pile
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
