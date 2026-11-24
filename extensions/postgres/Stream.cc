// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the rows of a selection read in batches
//
// the python face of this is an iterator over the batches, each one a result whose rows are the
// next few of the selection; a stream that goes away before its last batch is read stops the
// answer
void
pyre::postgres::py::stream(py::module & m)
{
    // the class
    auto cls = py::class_<Stream>(
        // in scope
        m,
        // the name
        "Stream",
        // the docstring
        "the rows of a selection, as an iterator over batches of them",
        // my destructor may wait for the session and for the server, so let go of the lock while
        // it runs
        py::release_gil_before_calling_cpp_dtor());

    // whether there may be rows still to come
    cls.def_property_readonly(
        // the name
        "live",
        // the implementation
        &Stream::live,
        // the docstring
        "whether there may be rows still to come");

    // the statement that started it
    cls.def_property_readonly(
        // the name
        "statement",
        // the implementation
        &Stream::statement,
        // the docstring
        "the statement that started the stream");

    // the number of rows it asked for in each batch
    cls.def_property_readonly(
        // the name
        "batch",
        // the implementation
        &Stream::batch,
        // the docstring
        "the number of rows the stream asked for in each batch");

    // the iterator protocol
    cls.def(
        // the name
        "__iter__",
        // the implementation; a stream is its own iterator, since its rows can be read only once
        [](py::object self) -> py::object { return self; },
        // the docstring
        "hand back the stream itself, which iterates over its batches");

    cls.def(
        // the name
        "__next__",
        // the implementation
        [](Stream & self) -> Result {
            // room for the batch
            std::optional<Result> batch;
            // in a scope of its own
            {
                // let go of the lock while the rows travel
                py::gil_scoped_release release;
                // wait for them
                batch = self.next();
            }
            // once the rows are all read
            if (!batch.has_value()) {
                // the iteration is over
                throw py::stop_iteration();
            }
            // otherwise, hand it off
            return std::move(*batch);
        },
        // the docstring
        "the next batch of rows, as a result");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Stream & self) -> string_t {
            return self.live() ? "<postgres.Stream: under way>" : "<postgres.Stream: ended>";
        },
        // the docstring
        "a human readable summary of this stream");

    // all done
    return;
}


// end of file
