// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the machinery this file needs, and nobody else does
namespace pyre::postgres::py {
    // every value in {row}, as a python tuple
    static auto values(const Row & row) -> py::tuple
    {
        // how many there are
        const auto columns = row.size();
        // room for them
        py::tuple rendering(columns);
        // fill it in
        for (size_type column = 0; column < columns; ++column) {
            // each value becomes a string, or {None} when the server sent nothing
            rendering[column] = pythonize(row[column]);
        }
        // hand it off
        return rendering;
    }

    // resolve a subscript into a column, the way python resolves one into a sequence
    static auto resolve(const Row & row, size_type column) -> size_type
    {
        // how many values there are
        const auto columns = row.size();
        // a negative subscript counts back from the end, which is what a python caller expects
        // and what the c++ class deliberately does not offer
        const size_type index = column < 0 ? column + columns : column;
        // and one that lands outside the row is an {IndexError}, and not one of ours; this is
        // the exception the iteration protocol and the slicing machinery both look for
        if (index < 0 || index >= columns) {
            throw py::index_error("row index out of range");
        }
        // hand it off
        return index;
    }
} // namespace pyre::postgres::py


// add the bindings for one row of a result set
//
// a row reads as a sequence of values, so that the record machinery in {pyre.db} may build a
// table row straight out of it. the fields behind those values are one call away, for a caller
// that wants to know what the server said their types were
void
pyre::postgres::py::row(py::module & m)
{
    // the class
    auto cls = py::class_<Row>(
        // in scope
        m,
        // the name
        "Row",
        // the docstring
        "one row of a result set, which reads as a sequence of its values");

    // where it came from
    cls.def_property_readonly(
        // the name
        "index",
        // the implementation
        &Row::index,
        // the docstring
        "my position in the result set");

    // how many values it holds
    cls.def(
        // the name
        "__len__",
        // the implementation
        &Row::size,
        // the docstring
        "the number of values i hold, which is the number of columns in the result set");

    // the value in a column, by position
    cls.def(
        // the name
        "__getitem__",
        // the implementation
        [](const Row & self, size_type column) -> py::object {
            return pythonize(self[resolve(self, column)]);
        },
        // the signature
        "column"_a,
        // the docstring
        "the value in the given {column}, or {None} when the server sent nothing");

    // and by name
    cls.def(
        // the name
        "__getitem__",
        // the implementation
        [](const Row & self, view_t name) -> py::object { return pythonize(self[name]); },
        // the signature
        "name"_a,
        // the docstring
        "the value in the column the server labeled {name}");

    // every value at once
    cls.def_property_readonly(
        // the name
        "values",
        // the implementation
        &values,
        // the docstring
        "all my values, as a tuple");

    // walking me walks my values, so that a row may stand wherever an iterable of them may
    cls.def(
        // the name
        "__iter__",
        // the implementation
        [](const Row & self) -> py::object { return py::iter(values(self)); },
        // the docstring
        "walk my values, left to right");

    // the field behind a value, by position
    cls.def(
        // the name
        "field",
        // the implementation
        [](const Row & self, size_type column) -> Field { return self[resolve(self, column)]; },
        // the signature
        "column"_a,
        // the docstring
        "the field in the given {column}, which knows its own name and type");

    // and by name
    cls.def(
        // the name
        "field",
        // the implementation
        [](const Row & self, view_t name) -> Field { return self[name]; },
        // the signature
        "name"_a,
        // the docstring
        "the field in the column the server labeled {name}");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Row & self) -> string_t {
            return "<postgres.Row " + std::to_string(self.index()) + ": "
                 + std::to_string(self.size()) + " values>";
        },
        // the docstring
        "a human readable summary of this row");

    // all done
    return;
}


// end of file
