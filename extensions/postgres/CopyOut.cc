// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the copy of rows out of the database
//
// the python face of this is an iterator over the lines of text the server sends; a copy that
// goes away before its last line is out asks the server to stop sending
void
pyre::postgres::py::copyOut(py::module & m)
{
    // the class
    auto cls = py::class_<CopyOut>(
        // in scope
        m,
        // the name
        "CopyOut",
        // the docstring
        "a copy of rows out of the database, as an iterator over its lines",
        // my destructor may wait for the session and for the server, so let go of the lock while
        // it runs
        py::release_gil_before_calling_cpp_dtor());

    // start one on a session
    cls.def(
        // the implementation
        py::init<Connection, view_t>(),
        // the signature
        "connection"_a, "statement"_a,
        // let go of the lock while the server starts it
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "start the copy {statement}, a COPY ... TO STDOUT, on {connection}");

    // whether there may be rows still to come
    cls.def_property_readonly(
        // the name
        "live",
        // the implementation
        &CopyOut::live,
        // the docstring
        "whether there may be rows still to come");

    // the statement that started it
    cls.def_property_readonly(
        // the name
        "statement",
        // the implementation
        &CopyOut::statement,
        // the docstring
        "the statement that started the copy");

    // the iterator protocol
    cls.def(
        // the name
        "__iter__",
        // the implementation; a copy is its own iterator, since its rows can be read only once
        [](py::object self) -> py::object { return self; },
        // the docstring
        "hand back the copy itself, which iterates over its rows");

    cls.def(
        // the name
        "__next__",
        // the implementation
        [](CopyOut & self) -> string_t {
            // room for the row
            std::optional<string_t> line;
            // in a scope of its own
            {
                // let go of the lock while the row travels
                py::gil_scoped_release release;
                // wait for it
                line = self.next();
            }
            // once the rows are all out
            if (!line.has_value()) {
                // the iteration is over
                throw py::stop_iteration();
            }
            // otherwise, hand it off
            return std::move(*line);
        },
        // the docstring
        "the next row, as a line of text");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const CopyOut & self) -> string_t {
            return self.live() ? "<postgres.CopyOut: under way>" : "<postgres.CopyOut: ended>";
        },
        // the docstring
        "a human readable summary of this copy");

    // all done
    return;
}


// end of file
