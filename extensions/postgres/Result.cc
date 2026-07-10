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
    // resolve a subscript into a row, the way python resolves one into a sequence
    static auto resolve(const Result & result, size_type row) -> size_type
    {
        // how many rows there are
        const auto rows = result.rows();
        // a negative subscript counts back from the end
        const size_type index = row < 0 ? row + rows : row;
        // and one that lands outside the result is an {IndexError}, and not one of ours
        if (index < 0 || index >= rows) {
            throw py::index_error("row index out of range");
        }
        // hand it off
        return index;
    }
} // namespace pyre::postgres::py


// add the bindings for everything the server sent back in answer to one statement
//
// a result reads as a sequence of rows, each of which reads as a sequence of values. the column
// names are a property of the result rather than its first row, which is where the bindings this
// package replaces used to put them: they returned a tuple whose head was the headers and whose
// tail was the data, and every caller had to know to skip it
void
pyre::postgres::py::result(py::module & m)
{
    // the class
    auto cls = py::class_<Result>(
        // in scope
        m,
        // the name
        "Result",
        // the docstring
        "everything the server sent back in answer to one statement");

    // how the statement turned out
    cls.def_property_readonly(
        // the name
        "status",
        // the implementation
        &Result::status,
        // the docstring
        "the state the server left the statement in");

    cls.def_property_readonly(
        // the name
        "ok",
        // the implementation
        &Result::ok,
        // the docstring
        "whether the statement ran");

    // shape
    cls.def(
        // the name
        "__len__",
        // the implementation
        &Result::rows,
        // the docstring
        "the number of rows the server sent");

    cls.def_property_readonly(
        // the name
        "rows",
        // the implementation
        &Result::rows,
        // the docstring
        "the number of rows the server sent");

    cls.def_property_readonly(
        // the name
        "columns",
        // the implementation
        &Result::columns,
        // the docstring
        "the number of values each row holds");

    // the column names, which live here rather than masquerading as the first row of the data
    cls.def_property_readonly(
        // the name
        "headers",
        // the implementation
        [](const Result & self) -> py::tuple {
            // how many there are
            const auto columns = self.columns();
            // room for them
            py::tuple names(columns);
            // fill it in
            for (size_type column = 0; column < columns; ++column) {
                names[column] = string_t(self.name(column));
            }
            // hand it off
            return names;
        },
        // the docstring
        "the labels the server gave my columns, as a tuple");

    // the position of a column, by name
    cls.def(
        // the name
        "column",
        // the implementation
        [](const Result & self, view_t name) -> size_type { return self.column(name); },
        // the signature
        "name"_a,
        // the docstring
        "the position of the column labeled {name}, or -1 when there is no such column");

    // the rows, by position
    cls.def(
        // the name
        "__getitem__",
        // the implementation
        [](const Result & self, size_type row) -> Row { return self[resolve(self, row)]; },
        // the signature
        "row"_a,
        // the docstring
        "the given {row}");

    // walking me walks my rows
    cls.def(
        // the name
        "__iter__",
        // the implementation
        [](const Result & self) -> py::object {
            // each row keeps the result set alive on its own, so nothing here needs a keep alive
            return py::make_iterator<py::return_value_policy::copy>(self.begin(), self.end());
        },
        // the docstring
        "walk my rows, top to bottom");

    // one value, reached directly
    cls.def(
        // the name
        "field",
        // the implementation
        [](const Result & self, size_type row, size_type column) -> Field {
            return self[resolve(self, row)].field(column);
        },
        // the signature
        "row"_a, "column"_a,
        // the docstring
        "the field in the given {row} and {column}");

    // what the server said about the statement itself
    cls.def_property_readonly(
        // the name
        "command",
        // the implementation
        [](const Result & self) -> string_t { return string_t(self.command()); },
        // the docstring
        "the tag the server put on the statement, e.g. 'INSERT 0 1'");

    cls.def_property_readonly(
        // the name
        "affected",
        // the implementation
        &Result::affected,
        // the docstring
        "how many rows the statement touched; zero for everything but insert, update and delete");

    cls.def_property_readonly(
        // the name
        "message",
        // the implementation
        [](const Result & self) -> string_t { return string_t(self.message()); },
        // the docstring
        "the one line rendering of whatever went wrong; empty when nothing did");

    cls.def_property_readonly(
        // the name
        "diagnostic",
        // the implementation
        [](const Result & self) -> Diagnostic { return self.diagnostic(); },
        // the docstring
        "the full report of what went wrong");

    // turn a failure into one
    cls.def(
        // the name
        "check",
        // the implementation
        [](const Result & self, view_t statement) -> void {
            // a statement that ran has nothing to complain about
            if (self.ok()) {
                return;
            }
            // and one that did not is classified by the name the server gave the condition; this
            // is how a caller draining an asynchronous statement turns its findings into failures
            self.raise(string_t(statement));
        },
        // the signature
        py::arg("statement") = "",
        // the docstring
        "raise the exception that names what went wrong, if anything did");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Result & self) -> string_t {
            return "<postgres.Result: " + std::to_string(self.rows()) + " rows of "
                 + std::to_string(self.columns()) + " columns>";
        },
        // the docstring
        "a human readable summary of this result set");

    // all done
    return;
}


// end of file
