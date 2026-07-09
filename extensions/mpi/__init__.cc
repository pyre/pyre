// -*- C++ -*-
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
    // the enumerations
    pyre::mpi::py::enums(m);

    // the structural entities; the communicator hands back groups, cartesian communicators and
    // conduits, so they must all be registered before anybody calls one of its methods, though
    // not before it is itself bound
    pyre::mpi::py::group(m);
    pyre::mpi::py::communicator(m);
    pyre::mpi::py::cartesian(m);
    pyre::mpi::py::port(m);

    // the module api, last, since its {world} hands back a communicator
    pyre::mpi::py::api(m);

    // all done
    return;
}


// end of file
