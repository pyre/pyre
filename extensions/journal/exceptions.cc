// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings to the inventory
void
pyre::journal::py::
exceptions(py::module & m) {
    // when {debug} channels are fatal
    py::register_exception<debug_error>(m, "DebugError");
    // when {firewalls} are fatal
    py::register_exception<firewall_error>(m, "FirewallError");
    // when user facing channels are fatal
    py::register_exception<application_error>(m, "ApplicationError");

    // all done
    return;
}


// end of file
