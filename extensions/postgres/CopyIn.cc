// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the copy of rows into a table
//
// the c++ class keeps the rows when {end} says so and throws them away when it goes away first,
// which python cannot promise to do on time. so the python face of this is a context manager,
// whose {__exit__} keeps the rows when the block finishes and throws them away when it raises
void
pyre::postgres::py::copyIn(py::module & m)
{
    // the class
    auto cls = py::class_<CopyIn>(
        // in scope
        m,
        // the name
        "CopyIn",
        // the docstring
        "a copy of rows into a table, as a context manager");

    // start one on a session
    cls.def(
        // the implementation
        py::init<Connection, view_t>(),
        // the signature
        "connection"_a, "statement"_a,
        // let go of the lock while the server starts it
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "start the copy {statement}, a COPY ... FROM STDIN, on {connection}");

    // whether it is under way
    cls.def_property_readonly(
        // the name
        "live",
        // the implementation
        &CopyIn::live,
        // the docstring
        "whether neither {end} nor {abort} has been called");

    // the statement that started it
    cls.def_property_readonly(
        // the name
        "statement",
        // the implementation
        &CopyIn::statement,
        // the docstring
        "the statement that started the copy");

    // send rows as text
    cls.def(
        // the name
        "put",
        // the implementation
        &CopyIn::put,
        // the signature
        "data"_a,
        // let go of the lock while the rows travel
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "send {data}, any number of whole rows in the text format of a copy");

    // send one row of python values
    cls.def(
        // the name
        "row",
        // the implementation
        [](CopyIn & self, const py::args & args) -> void {
            // render the values while we still hold the lock, as {Connection.execute} does
            const auto rendered = arguments(args);
            // and let go of it while the row travels
            py::gil_scoped_release release;
            // send it
            self.row(rendered);
            // all done
            return;
        },
        // the docstring
        "send one row, whose values are rendered as the text their columns read; {None} is NULL");

    // keep the rows
    cls.def(
        // the name
        "end",
        // the implementation
        &CopyIn::end,
        // let go of the lock while the server works
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "keep the rows, and hand back what the server said, which counts them");

    // throw them away
    cls.def(
        // the name
        "abort",
        // the implementation
        &CopyIn::abort,
        // the signature
        "reason"_a,
        // let go of the lock while the server works
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "throw the rows away, giving the server {reason}");

    // the context manager protocol
    cls.def(
        // the name
        "__enter__",
        // the implementation; hand back the very object the {with} statement was given, so that
        // its {as} clause binds to something whose lifetime the interpreter is already managing
        [](py::object self) -> py::object { return self; },
        // the docstring
        "hook invoked when the context manager is entered");

    cls.def(
        // the name
        "__exit__",
        // the implementation
        [](CopyIn & self, const py::object & type, const py::object &, const py::object &) -> bool {
            // somebody inside the block has already ended me
            if (!self.live()) {
                // so there is nothing left to do
                return false;
            }
            // whether the block ran to the end
            const auto finished = type.is_none();
            // let go of the lock while the server works
            py::gil_scoped_release release;
            // a block that ran to the end
            if (finished) {
                // keeps its rows, which raises when the server refuses them
                self.end();
            }
            // and one that raised
            else {
                // throws them away
                self.abort("the block of the copy raised an exception");
            }

            // in either case, say nothing about the exception; one that was raised inside the
            // block is one the caller asked to see
            return false;
        },
        // the signature
        "type"_a, "value"_a, "traceback"_a,
        // the docstring
        "hook invoked when the context manager's block exits");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const CopyIn & self) -> string_t {
            return self.live() ? "<postgres.CopyIn: under way>" : "<postgres.CopyIn: ended>";
        },
        // the docstring
        "a human readable summary of this copy");

    // all done
    return;
}


// end of file
