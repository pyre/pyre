// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for one value in a result set
//
// a field keeps its result set alive on its own, so one may be pulled out of a result and kept
// long after the result itself has been let go
void
pyre::postgres::py::field(py::module & m)
{
    // the class
    auto cls = py::class_<Field>(
        // in scope
        m,
        // the name
        "Field",
        // the docstring
        "one value in a result set, together with what its column says it means");

    // where it came from
    cls.def_property_readonly(
        // the name
        "row",
        // the implementation
        &Field::row,
        // the docstring
        "the row i came from");

    cls.def_property_readonly(
        // the name
        "column",
        // the implementation
        &Field::column,
        // the docstring
        "the column i came from");

    cls.def_property_readonly(
        // the name
        "name",
        // the implementation
        [](const Field & self) -> string_t { return string_t(self.name()); },
        // the docstring
        "the label the server gave my column");

    cls.def_property_readonly(
        // the name
        "type",
        // the implementation
        &Field::type,
        // the docstring
        "the identifier of my type, as postgres catalogs it");

    cls.def_property_readonly(
        // the name
        "format",
        // the implementation
        &Field::format,
        // the docstring
        "whether my bytes are text or the internal representation of my type");

    // what it holds
    cls.def_property_readonly(
        // the name
        "isNull",
        // the implementation
        &Field::isNull,
        // the docstring
        "whether the server sent nothing at all; a NULL is not the empty string");

    cls.def_property_readonly(
        // the name
        "size",
        // the implementation
        &Field::size,
        // the docstring
        "the number of octets in my value");

    cls.def_property_readonly(
        // the name
        "value",
        // the implementation
        [](const Field & self) -> py::object { return pythonize(self); },
        // the docstring
        "my value as a string, or {None} when the server sent nothing");

    cls.def_property_readonly(
        // the name
        "bytes",
        // the implementation
        [](const Field & self) -> py::object {
            // a value that is not there has no octets either
            if (self.isNull()) {
                return py::none();
            }
            // and one that is arrives exactly as the server sent it, uninterpreted; this is the
            // way to reach a column the server was asked to send in its binary format
            const auto octets = self.bytes();
            return py::bytes(octets.data(), octets.size());
        },
        // the docstring
        "my value as raw octets, or {None} when the server sent nothing");

    // contextual conversion to {bool}, true when i hold a value
    cls.def(
        // the name
        "__bool__",
        // the implementation
        [](const Field & self) -> bool { return !self.isNull(); },
        // the docstring
        "whether i hold a value; a field holding {False} still holds something");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Field & self) -> string_t {
            // name the column, and say whether there is anything in it
            string_t rendering = "<postgres.Field '";
            rendering += self.name();
            rendering += "': ";
            rendering += self.isNull() ? "NULL" : string_t(self.bytes());
            rendering += ">";
            return rendering;
        },
        // the docstring
        "a human readable summary of this value");

    // all done
    return;
}


// end of file
