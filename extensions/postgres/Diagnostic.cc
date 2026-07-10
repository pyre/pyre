// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for everything the server says about a statement that did not work out
//
// an exception carries this across as a set of attributes, because that is the shape the python
// hierarchy has always had. this class is here for the other path: a result harvested from an
// asynchronous statement is handed back whatever it says, and this is how a caller reads it
void
pyre::postgres::py::diagnostic(py::module & m)
{
    // the class
    auto cls = py::class_<Diagnostic>(
        // in scope
        m,
        // the name
        "Diagnostic",
        // the docstring
        "everything the server said about a statement that did not work out");

    // the statement we sent
    cls.def_property_readonly(
        // the name
        "command",
        // the implementation
        &Diagnostic::command,
        // the docstring
        "the sql that provoked this report");

    // how bad the server thinks this is
    cls.def_property_readonly(
        // the name
        "severity",
        // the implementation
        &Diagnostic::severity,
        // the docstring
        "one of ERROR, FATAL, PANIC, WARNING, NOTICE, INFO, DEBUG or LOG, always in english");

    // the name of the condition
    cls.def_property_readonly(
        // the name
        "sqlstate",
        // the implementation
        &Diagnostic::sqlstate,
        // the docstring
        "the five character code that names the condition; the only portable part of a complaint");

    // the family it belongs to
    cls.def_property_readonly(
        // the name
        "category",
        // the implementation
        [](const Diagnostic & self) -> string_t { return string_t(self.category()); },
        // the docstring
        "the first two characters of the {sqlstate}, which name the family of the condition");

    // the one line explanation
    cls.def_property_readonly(
        // the name
        "message",
        // the implementation
        &Diagnostic::message,
        // the docstring
        "the explanation the server wrote, for a human");

    // the elaborations
    cls.def_property_readonly(
        // the name
        "detail",
        // the implementation
        &Diagnostic::detail,
        // the docstring
        "a second paragraph, with the particulars; empty when the server sent none");

    cls.def_property_readonly(
        // the name
        "hint",
        // the implementation
        &Diagnostic::hint,
        // the docstring
        "the server's suggestion for how to resolve the problem, when it offered one");

    cls.def_property_readonly(
        // the name
        "position",
        // the implementation
        &Diagnostic::position,
        // the docstring
        "where in {command} the server gave up, counting from one; zero when it did not say");

    cls.def_property_readonly(
        // the name
        "context",
        // the implementation
        &Diagnostic::context,
        // the docstring
        "the call stack in the server's terms: a function, a trigger, a cursor");

    // the object the complaint is about
    cls.def_property_readonly(
        // the name
        "schema",
        // the implementation
        &Diagnostic::schema,
        // the docstring
        "the schema the offending object lives in");

    cls.def_property_readonly(
        // the name
        "table",
        // the implementation
        &Diagnostic::table,
        // the docstring
        "the table the complaint is about");

    cls.def_property_readonly(
        // the name
        "column",
        // the implementation
        &Diagnostic::column,
        // the docstring
        "the column the complaint is about");

    cls.def_property_readonly(
        // the name
        "datatype",
        // the implementation
        &Diagnostic::datatype,
        // the docstring
        "the type the complaint is about");

    cls.def_property_readonly(
        // the name
        "constraint",
        // the implementation
        &Diagnostic::constraint,
        // the docstring
        "the constraint that was violated; this is how two unique indices are told apart");

    // the interactive representation
    cls.def(
        // the name
        "__str__",
        // the implementation
        &Diagnostic::describe,
        // the docstring
        "the one line rendering of this report");

    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Diagnostic & self) -> string_t {
            return "<postgres.Diagnostic: " + self.describe() + ">";
        },
        // the docstring
        "a human readable summary of this report");

    // all done
    return;
}


// end of file
