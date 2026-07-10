// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external dependencies, and the aliases that shape this namespace
#include "external.h"


// the {postgres} extension namespace
namespace pyre::postgres::py {
    // the exception hierarchy, translated into the one {pyre.db} already publishes
    void exceptions(py::module & m);
    // the enumerations: the states the server reports, and the layout of the values it sends
    void enums(py::module & m);

    // what the server says about a statement that did not work out
    void diagnostic(py::module & m);

    // what it sends back when one does
    void field(py::module & m);
    void row(py::module & m);
    void result(py::module & m);

    // what other sessions have to say
    void notification(py::module & m);

    // the session, and the scope of the work done over it
    void connection(py::module & m);
    void transaction(py::module & m);

    // loose functions: the module metadata, and the rendering of python values as the text
    // postgres reads
    void utilities(py::module & m);
} // namespace pyre::postgres::py


// the machinery the bindings share
namespace pyre::postgres::py {
    // turn a python object into the text that fills one placeholder of a statement; {None}
    // becomes the {NULL} that no text can spell
    auto render(py::handle value) -> argument_t;
    // turn the value of {field} into a python object; a {NULL} becomes {None}, which is what
    // the database api asks for and what the sqlite back end already does
    auto pythonize(const Field & field) -> py::object;
    // turn every argument of a call into the text of a statement's placeholders
    auto arguments(const py::args & args) -> arguments_t;
} // namespace pyre::postgres::py


// end of file
