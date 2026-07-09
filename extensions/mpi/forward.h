// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external dependencies, and the aliases that shape this namespace
#include "external.h"


// the {libmpi} extension namespace
namespace pyre::mpi::py {
    // the module api: bringing mpi up and down, and the entities it predefines
    void api(py::module & m);
    // the enumerations: the reduction operators, and the outcome of a comparison
    void enums(py::module & m);
    // the exception hierarchy, translated into python
    void exceptions(py::module & m);

    // what mpi reports about a transfer, finished or not
    void status(py::module & m);
    void request(py::module & m);

    // the structural entities
    void group(py::module & m);
    void communicator(py::module & m);
    void cartesian(py::module & m);

    // the python level conduit
    void port(py::module & m);
} // namespace pyre::mpi::py


// end of file
