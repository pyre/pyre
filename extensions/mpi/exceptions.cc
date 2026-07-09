// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// register the exception hierarchy with python
//
// every entry point below can throw, and nothing that {pyre::mpi} raises may cross into python
// unhandled, so each of its three exception types gets a counterpart to arrive as
void
pyre::mpi::py::exceptions(py::module & m)
{
    // the base of everything the package raises; it derives from python's {Exception}
    auto error = py::register_exception<Error>(m, "Error");
    // a failed mpi call
    py::register_exception<MPIError>(m, "MPIError", error);
    // an argument whose shape does not match what the call requires
    py::register_exception<ShapeError>(m, "ShapeError", error);

    // the order matters: pybind tries its translators in reverse, so the two derived types
    // must be registered after their base if a {ShapeError} is to reach python under its own
    // name rather than its parent's

    // all done
    return;
}


// end of file
