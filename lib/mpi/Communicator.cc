// -*- C++ -*-
//
//
// michael a.g. aivazis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#include <portinfo>

#include <mpi.h>
// #include "journal/diagnostics.h"

// local
#include "Group.h"
#include "Communicator.h"


// factory
pyre::mpi::Communicator * pyre::mpi::Communicator::newCommunicator(const Group & group) const {
    MPI_Comm oldHandle = _communicator;
    MPI_Group groupHandle = group.handle();
        
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
        
#if 0
    journal::debug_t info("mpi.init");
    info
        << journal::at(__HERE__)
        << "[" << rank << ":" << size << "] "
        << "creating communicator: "
        << "old=" << oldHandle << ", group=" << groupHandle
        << journal::endl;
#endif

    MPI_Comm comm;
    int status = MPI_Comm_create(oldHandle, groupHandle, &comm);
    if (status != MPI_SUCCESS) {
#if 0
        journal::error_t error("mpi.init");

        error
            << journal::at(__HERE__)
            << "[" << rank << ":" << size << "] "
            << "mpi failure " << status << " while creating communicator: "
            << "old=" << oldHandle << ", group=" << groupHandle
            << journal::endl;
#endif
        return 0;
    }

    if (comm ==  MPI_COMM_NULL) {
        return 0;
    }

    return new Communicator(comm);
}


pyre::mpi::Communicator * 
pyre::mpi::Communicator::cartesian(int size, int * procs, int * periods, int reorder) const {
    MPI_Comm cartesian;
    int status = MPI_Cart_create(_communicator, size, procs, periods, reorder, &cartesian);
    if (status != MPI_SUCCESS) {
#if 0
        journal::error_t error("mpi.cartesian");
        error 
            << journal::at(__HERE__)
            << "MPI_Comm_create: error " << status
            << journal::endl;
#endif
        return 0;
    }

    if (cartesian == MPI_COMM_NULL) {
#if 0
        journal::error_t error("mpi.cartesian");
        error 
            << journal::at(__HERE__)
            << "MPI_Comm_create: error: null cartesian communicator"
            << journal::endl;
#endif
        return 0;
    }

    return new Communicator(cartesian);
}


// interface

int pyre::mpi::Communicator::size() const {
    int size;
    int status = MPI_Comm_size(_communicator, &size);
    if (status != MPI_SUCCESS) {
        return -1;
        }

    return size;
}


int pyre::mpi::Communicator::rank() const {
    int rank;
    int status = MPI_Comm_rank(_communicator, &rank);
    if (status != MPI_SUCCESS) {
#if 0
        journal::error_t error("mpi.cartesian");
        error 
            << journal::at(__HERE__)
            << "MPI_Comm_rank: error " << status
            << journal::endl;
#endif
        return -1;
    }

    return rank;
}


void pyre::mpi::Communicator::barrier() const
{
    int status = MPI_Barrier(_communicator);
    if (status != MPI_SUCCESS) {
#if 0
        journal::error_t error("mpi.cartesian");
        error 
            << journal::at(__HERE__)
            << "MPI_Barrier: error " << status
            << journal::endl;
#endif

        return;
    }

    return;
}


MPI_Comm pyre::mpi::Communicator::handle() const
{
    return _communicator;
}


void pyre::mpi::Communicator::cartesianCoordinates(int rank, int dim, int * coordinates) const {
    int status = MPI_Cart_coords(_communicator, rank, dim, coordinates);
    if (status != MPI_SUCCESS) {
#if 0
        journal::error_t error("mpi.cartesian");
        error 
            << journal::at(__HERE__)
            << "MPI_Cart_coords: error " << status
            << journal::endl;
#endif

        return;
    }

#if 0
    journal::debug_t info("mpi.cartesian");
    info << journal::at(__HERE__) << "coordinates:";
    for (int i=0; i < dim; ++i) {
        info << " " << coordinates[i];
    }
    info << journal::endl;
#endif

    return;
}


// constructors
pyre::mpi::Communicator::Communicator(MPI_Comm handle):
    _communicator(handle)
{}


// destructor
pyre::mpi::Communicator::~Communicator() {
    MPI_Comm_free(&_communicator);
}

// end of file
