// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for pipelines of statements
//
// the python face of this is a context manager that sends statements without waiting for the
// answers to the ones before them, and an iterator over their results, in the order they were
// sent; the end of the block ends the pipeline, reading whatever answers were left unread
void
pyre::postgres::py::pipeline(py::module & m)
{
    // the class
    auto cls = py::class_<Pipeline>(
        // in scope
        m,
        // the name
        "Pipeline",
        // the docstring
        "a pipeline of statements, and an iterator over their results");

    // send a statement
    cls.def(
        // the name
        "execute",
        // the implementation
        [](Pipeline & self, view_t statement, const py::args & args) -> void {
            // render the arguments while we still hold the lock
            const auto rendered = arguments(args);
            // and let go of it while the statement goes out
            py::gil_scoped_release release;
            // send it
            self.execute(statement, rendered);
        },
        // the signature
        "statement"_a,
        // the docstring
        "send {statement}, with its $1, $2, ... placeholders filled in from the {arguments}");

    // teach the server a statement
    cls.def(
        // the name
        "prepare",
        // the implementation
        &Pipeline::prepare,
        // the signature
        "name"_a, "statement"_a,
        // let go of the lock while the statement goes out
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "teach the server {statement} under the given {name}");

    // run what it was taught
    cls.def(
        // the name
        "execPrepared",
        // the implementation
        [](Pipeline & self, view_t name, const py::args & args) -> void {
            // render the arguments while we still hold the lock
            const auto rendered = arguments(args);
            // and let go of it while the statement goes out
            py::gil_scoped_release release;
            // send it
            self.execPrepared(name, rendered);
        },
        // the signature
        "name"_a,
        // the docstring
        "run the statement the server was taught under {name}, with its placeholders filled in");

    // end a segment
    cls.def(
        // the name
        "sync",
        // the implementation
        &Pipeline::sync,
        // let go of the lock while the mark goes out
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "end the segment of the statements sent since the last sync");

    // end the pipeline
    cls.def(
        // the name
        "close",
        // the implementation
        &Pipeline::close,
        // let go of the lock while the answers are read to the end
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "end the pipeline: sync what was sent, read the answers to the end, and let go of the "
        "session");

    // the statements waiting for their answers
    cls.def_property_readonly(
        // the name
        "pending",
        // the implementation
        &Pipeline::pending,
        // the docstring
        "the number of statements sent whose answers have not been read");

    // whether it holds the session
    cls.def_property_readonly(
        // the name
        "live",
        // the implementation
        &Pipeline::live,
        // the docstring
        "whether the pipeline holds its session");

    // the iterator protocol
    cls.def(
        // the name
        "__iter__",
        // the implementation; a pipeline is its own iterator, since its answers can be read once
        [](py::object self) -> py::object { return self; },
        // the docstring
        "hand back the pipeline itself, which iterates over the answers to its statements");

    cls.def(
        // the name
        "__next__",
        // the implementation
        [](Pipeline & self) -> Result {
            // room for the answer
            std::optional<Result> answer;
            // in a scope of its own
            {
                // let go of the lock while the answer travels
                py::gil_scoped_release release;
                // wait for it
                answer = self.next();
            }
            // once every statement has been answered
            if (!answer.has_value()) {
                // the iteration is over
                throw py::stop_iteration();
            }
            // otherwise, hand it off
            return std::move(*answer);
        },
        // the docstring
        "the answer to the next statement, as a result");

    // the context manager protocol
    cls.def(
        // the name
        "__enter__",
        // the implementation
        [](py::object self) -> py::object { return self; },
        // the docstring
        "hand back the pipeline for the length of a block");

    cls.def(
        // the name
        "__exit__",
        // the implementation
        [](Pipeline & self, py::args) -> bool {
            // let go of the lock while the pipeline ends
            py::gil_scoped_release release;
            // end it
            self.close();
            // and let whatever the block raised go on
            return false;
        },
        // the docstring
        "end the pipeline when the block ends");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Pipeline & self) -> string_t {
            return self.live() ? "<postgres.Pipeline: under way>" : "<postgres.Pipeline: ended>";
        },
        // the docstring
        "a human readable summary of this pipeline");

    // all done
    return;
}


// end of file
