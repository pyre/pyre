// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings to the inventory
void
pyre::journal::py::
exceptions(py::module & m) {
    // get the base exception as a raw {PyObject *}, which is what {register_exception} wants
    auto journalError =
        py::module::import("journal").attr("exceptions").attr("JournalError").ptr();

    // when {debug} channels are fatal
    py::register_exception<debug_error>(m, "DebugError", journalError);
    // when {firewalls} are fatal
    py::register_exception<firewall_error>(m, "FirewallError", journalError);
    // when user facing channels are fatal
    py::register_exception<application_error>(m, "ApplicationError", journalError);

    // all done
    return;
}


// end of file
