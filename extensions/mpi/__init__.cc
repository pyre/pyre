// -*- c++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2026 all rights reserved
//

// externals
#include "external.h"
// subsystem binders
#include "forward.h"


// the module entry point
PYBIND11_MODULE(mpi, m)
{
    // documentation
    m.doc() = "access to the MPI interface";
    // metadata
    m.attr("version")   = "1.0";
    m.attr("copyright") = "mpi: (c) 1998-2026 Michael A.G. Aïvázis";

    // MPI constants
    m.attr("undefined")  = MPI_UNDEFINED;
    m.attr("any_tag")    = MPI_ANY_TAG;
    m.attr("any_source") = MPI_ANY_SOURCE;

    // register the MPI error exception
    py::register_exception<pyre::mpi::py::Error>(m, "Error");

    // bind subsystems in dependency order:
    // Communicator and Group must be registered before they are used as argument/return types
    pyre::mpi::py::communicator(m);
    pyre::mpi::py::group(m);
    pyre::mpi::py::ports(m);
    pyre::mpi::py::startup(m);

    // add the world communicator (immortal=true: MPI_COMM_WORLD must never be freed)
    m.attr("world") = pyre::mpi::Communicator(MPI_COMM_WORLD, true);
}


// end of file
