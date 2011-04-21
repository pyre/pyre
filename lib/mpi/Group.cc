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

// interface
MPI_Group pyre::mpi::Group::handle() const {
    return _group;
}


int pyre::mpi::Group::size() const {
    int size;
    int status = MPI_Group_size(_group, &size);
    if (status != MPI_SUCCESS) {
        return -1;
    }

    return size;
}


int pyre::mpi::Group::rank() const {
    int rank;
    int status = MPI_Group_rank(_group, &rank);
    if (status != MPI_SUCCESS) {
        return -1;
    }

    return rank;
}


pyre::mpi::Group *
pyre::mpi::Group::newGroup(const pyre::mpi::Communicator & comm) {

    MPI_Comm commHandle = comm.handle();

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

#if 0
    journal::debug_t info("mpi.init");
    info
        << journal::at(__HERE__)
        << "[" << rank << ":" << size << "] "
        << "creating communicator gourp: "
        << "communicator=" << commHandle
        << journal::endl;
#endif
        
    MPI_Group group;
    int status = MPI_Comm_group(commHandle, &group);
    if (status != MPI_SUCCESS) {
#if 0
        journal::error_t error("mpi.init");
        error
            << journal::at(__HERE__)
            << "[" << rank << ":" << size << "] "
            << "mpi failure " << status << " while creating communicator group: "
            << "communicator=" << commHandle
            << journal::endl;
#endif
        return 0;
    }

    if (group == MPI_GROUP_NULL) {
        return 0;
    }

    // return
    return new Group(group);
}
    
    
pyre::mpi::Group * pyre::mpi::Group::include(int size, int ranks []) const {
    MPI_Group newGroup = MPI_GROUP_NULL;
    int status = MPI_Group_incl(_group, size, ranks, &newGroup);

    if (status != MPI_SUCCESS) {
        return 0;
    }

    if (newGroup == MPI_GROUP_NULL) {
        return 0;
    }

    return new Group(newGroup);
}
    

pyre::mpi::Group * pyre::mpi::Group::exclude(int size, int ranks []) const {
    MPI_Group newGroup = MPI_GROUP_NULL;
    int status = MPI_Group_excl(_group, size, ranks, &newGroup);

    if (status != MPI_SUCCESS) {
        return 0;
    }

    if (newGroup == MPI_GROUP_NULL) {
        return 0;
    }

    return new Group(newGroup);
}


// constructor
pyre::mpi::Group::Group(MPI_Group handle):
    _group(handle)
{}


// destructor
pyre::mpi::Group::~Group() {
    MPI_Group_free(&_group);
}

// end of file
    
