// -*- c++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2026 all rights reserved
//

// externals
#include "external.h"


namespace pyre::mpi::py {

void
startup(::py::module & m)
{
    // initialize MPI
    m.def(
        "init",
        []() {
            // check whether MPI is already initialized
            int isInitialized = 0;
            if (MPI_Initialized(&isInitialized) != MPI_SUCCESS) {
                throw pyre::mpi::py::Error("error while checking MPI initialization state");
            }
            // if not already initialized
            if (!isInitialized) {
                // no need to hunt down {argc, argv}: {mpirun} does all the work
                MPI_Init(0, 0);
            }
            // build a channel
            pyre::journal::debug_t channel("mpi.init");
            if (channel) {
                int rank, size;
                MPI_Comm_rank(MPI_COMM_WORLD, &rank);
                MPI_Comm_size(MPI_COMM_WORLD, &size);
                channel << pyre::journal::at(__HERE__)
                        << "[" << rank << ":" << size << "] "
                        << "mpi initialized successfully" << pyre::journal::endl;
            }
        },
        "initialize MPI");

    // finalize MPI
    m.def(
        "finalize",
        []() {
            int isInitialized = 0;
            if (MPI_Initialized(&isInitialized) != MPI_SUCCESS) {
                throw pyre::mpi::py::Error("MPI_Initialized failed");
            }
            int isFinalized = 0;
            if (MPI_Finalized(&isFinalized) != MPI_SUCCESS) {
                throw pyre::mpi::py::Error("MPI_Finalized failed");
            }
            if (isInitialized && !isFinalized) {
                int rank, size;
                MPI_Comm_rank(MPI_COMM_WORLD, &rank);
                MPI_Comm_size(MPI_COMM_WORLD, &size);
                int success = MPI_Finalize();
                pyre::journal::debug_t channel("mpi.init");
                channel << pyre::journal::at(__HERE__)
                        << "[" << rank << ":" << size << "] "
                        << "finalized mpi; status = " << success << pyre::journal::endl;
            }
        },
        "shut down MPI");
}

} // namespace pyre::mpi::py


// end of file
