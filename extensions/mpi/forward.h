// -*- c++ -*-
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

    // register the classes of what mpi reports about a transfer, finished or not
    void statusClass(py::module & m);
    void requestClass(py::module & m);
    // of the structural entities
    void groupClass(py::module & m);
    void communicatorClass(py::module & m);
    void cartesianClass(py::module & m);
    // and of the python level conduit
    void portClass(py::module & m);

    // what mpi reports about a transfer, finished or not
    void status();
    void request(py::module & m);

    // the structural entities
    void group();
    void communicator();
    void cartesian();

    // the python level conduit
    void port();
} // namespace pyre::mpi::py


// end of file
