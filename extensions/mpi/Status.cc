// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for what mpi reports about a completed transfer
void
pyre::mpi::py::status(py::module & m)
{
    // the class
    auto cls = py::class_<Status>(
        // in scope
        m,
        // the name
        "Status",
        // the docstring
        "what mpi reports about a message transfer that has completed");

    // who sent the message
    cls.def_property_readonly(
        // the name
        "source",
        // the implementation
        &Status::source,
        // the docstring
        "the rank of the process that sent the message");

    // the label it carried
    cls.def_property_readonly(
        // the name
        "tag",
        // the implementation
        &Status::tag,
        // the docstring
        "the label the message carried");

    // whether the transfer failed
    cls.def_property_readonly(
        // the name
        "error",
        // the implementation
        &Status::error,
        // the docstring
        "the status code of the transfer itself");

    // whether it was cancelled
    cls.def_property_readonly(
        // the name
        "cancelled",
        // the implementation
        &Status::cancelled,
        // the docstring
        "whether the transfer was cancelled before it could complete");

    // how much arrived; every payload that crosses into python is a stream of octets, so this
    // is the only count worth publishing
    cls.def_property_readonly(
        // the name
        "bytes",
        // the implementation
        [](const Status & self) -> size_type { return self.count(MPI_BYTE); },
        // the docstring
        "the number of octets the message held");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Status & self) -> string_t {
            return "<mpi.Status: source " + std::to_string(self.source()) + ", tag "
                 + std::to_string(self.tag()) + ">";
        },
        // the docstring
        "a human readable summary of this report");

    // all done
    return;
}


// end of file
