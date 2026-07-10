// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the scope of a transaction
//
// the c++ class ties the transaction to the lifetime of an object, which python cannot promise:
// its objects go away when the last reference to them does, and that may be a long time after the
// block they were built in. so the python face of this is a context manager, whose {__exit__} runs
// exactly where the destructor would have
void
pyre::postgres::py::transaction(py::module & m)
{
    // the class
    auto cls = py::class_<Transaction>(
        // in scope
        m,
        // the name
        "Transaction",
        // the docstring
        "the scope of a transaction, as a context manager");

    // open one on a session
    cls.def(
        // the implementation
        py::init<Connection>(),
        // the signature
        "connection"_a,
        // let go of the lock while the server opens it
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "open a transaction on {connection}");

    // whether it is still open
    cls.def_property_readonly(
        // the name
        "live",
        // the implementation
        &Transaction::live,
        // the docstring
        "whether neither {commit} nor {rollback} has been called");

    // make everything done inside it permanent
    cls.def(
        // the name
        "commit",
        // the implementation
        &Transaction::commit,
        // let go of the lock while the server works
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "make everything done inside me permanent");

    // and undo it instead
    cls.def(
        // the name
        "rollback",
        // the implementation
        &Transaction::rollback,
        // let go of the lock while the server works
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "undo everything done inside me");

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
        [](Transaction & self, const py::object & type, const py::object &,
           const py::object &) -> bool {
            // somebody inside the block has already closed me
            if (!self.live()) {
                // so there is nothing left to do
                return false;
            }
            // the block ran to the end
            if (type.is_none()) {
                // so keep what it did
                self.commit();
            }
            // and otherwise it threw
            else {
                // so undo it
                self.rollback();
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
        [](const Transaction & self) -> string_t {
            return self.live() ? "<postgres.Transaction: open>"
                               : "<postgres.Transaction: closed>";
        },
        // the docstring
        "a human readable summary of this transaction");

    // all done
    return;
}


// end of file
