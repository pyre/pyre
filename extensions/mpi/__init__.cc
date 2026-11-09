// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
//
// note that the module does not bring mpi up as it is imported. a process may not fork and exec
// {mpirun} after it has called {MPI_Init}, which openmpi has discouraged forever and forbidden
// outright since its version 3.0. so the launcher builds the parallel machine first, and only
// then does somebody call {initialize}
PYBIND11_MODULE(libmpi, m)
{
    // the docstring
    m.doc() = "the mpi extension module";

    // the exception hierarchy, first, so that everything registered below it can raise
    pyre::mpi::py::exceptions(m);
    // the enumerations, next, since the default arguments below name their values
    pyre::mpi::py::enums(m);

    // register every class before binding any interface, since the signatures name the
    // classes they traffic in, and the communicator hands back groups, cartesian communicators
    // and conduits: what mpi reports about a transfer, finished or not
    pyre::mpi::py::statusClass(m);
    pyre::mpi::py::requestClass(m);
    // the structural entities, the base communicator before the cartesian one that derives
    // from it
    pyre::mpi::py::groupClass(m);
    pyre::mpi::py::communicatorClass(m);
    pyre::mpi::py::cartesianClass(m);
    // and the python level conduit
    pyre::mpi::py::portClass(m);

    // now bind their interfaces: what mpi reports about a transfer
    pyre::mpi::py::status();
    pyre::mpi::py::request(m);
    // the structural entities
    pyre::mpi::py::group();
    pyre::mpi::py::communicator();
    pyre::mpi::py::cartesian();
    // and the conduit
    pyre::mpi::py::port();

    // the module api, last, since its {world} hands back a communicator
    pyre::mpi::py::api(m);

    // all done
    return;
}


// end of file
