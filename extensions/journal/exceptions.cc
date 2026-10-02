// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// raise the python counterpart of a journal exception
template <class errorT>
static void
raise(const char * type, const errorT & error)
{
    // build the exception
    auto complaint = pyre::journal::py::complaint(type, error);
    // and hand it to the interpreter
    PyErr_SetObject(reinterpret_cast<PyObject *>(Py_TYPE(complaint.ptr())), complaint.ptr());
    // all done
    return;
}


// add bindings to the inventory
void
pyre::journal::py::exceptions(py::module & m)
{
    // the exception classes live in the python package, so both implementations share them
    auto exceptions = py::module::import("journal.exceptions");
    // publish them
    m.attr("DebugError") = exceptions.attr("DebugError");
    m.attr("FirewallError") = exceptions.attr("FirewallError");
    m.attr("ApplicationError") = exceptions.attr("ApplicationError");

    // translate the journal exceptions that cross into python
    py::register_exception_translator([](std::exception_ptr pending) -> void {
        // carefully
        try {
            // if there is an exception in flight
            if (pending) {
                // raise it again so we can tell what it is
                std::rethrow_exception(pending);
            }
        }
        // when {debug} channels are fatal
        catch (const debug_error & error) {
            // raise the python counterpart
            raise("DebugError", error);
        }
        // when {firewalls} are fatal
        catch (const firewall_error & error) {
            // raise the python counterpart
            raise("FirewallError", error);
        }
        // when user facing channels are fatal
        catch (const application_error & error) {
            // raise the python counterpart
            raise("ApplicationError", error);
        }
        // all done
        return;
    });

    // all done
    return;
}


// end of file
