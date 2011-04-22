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
#include "Error.h"
#include "Group.h"
#include "Communicator.h"

// interface

// build the group that is associated with the given communicator
pyre::mpi::Group *
pyre::mpi::Group::
newGroup(const pyre::mpi::Communicator & communicator) {
    // get the raw MPI communicator
    MPI_Comm handle = communicator.handle();
    // and its associated group
    MPI_Group group;
    int status = MPI_Comm_group(handle, &group);
    // convert MPI failures to exceptions
    if (status != MPI_SUCCESS) {
        throw(Error(status));
    }
    // if the new group is empty
    if (group == MPI_GROUP_EMPTY) {
        // return the empty singleton
        return empty;
    }
    // otherwise, wrap the handle and return
    return new Group(group);
}
    
    
// build a group by including only the processes in {ranks}
pyre::mpi::Group * pyre::mpi::Group::include(int size, int ranks []) const {
    // build the new group
    MPI_Group newGroup;
    int status = MPI_Group_incl(_group, size, ranks, &newGroup);
    // convert MPI failures to exceptions
    if (status != MPI_SUCCESS) {
        throw(Error(status));
    }
    // if the new group is empty
    if (newGroup == MPI_GROUP_EMPTY) {
        // return the empty singleton
        return empty;
    }
    // otherwise, wrap the new handle and return it
    return new Group(newGroup);
}
    

// build a group by excluding the processes in {ranks}
pyre::mpi::Group * pyre::mpi::Group::exclude(int size, int ranks []) const {
    // build the new group
    MPI_Group newGroup;
    int status = MPI_Group_excl(_group, size, ranks, &newGroup);
    // if the MPI call failed
    if (status != MPI_SUCCESS) {
        throw(Error(status));
    }
    // if the new group is empty
    if (newGroup == MPI_GROUP_EMPTY) {
        // return the empty singleton
        return empty;
    }
    // otherwise, wrap the new handle and return it
    return new Group(newGroup);
}


// build a group from the union of two others
pyre::mpi::Group *
pyre::mpi::groupUnion(const pyre::mpi::Group * a, const pyre::mpi::Group * b) {
    // the new group
    MPI_Group newGroup;
    int status = MPI_Group_union(a->handle(), b->handle(), &newGroup);
    // if the MPI call failed
    if (status != MPI_SUCCESS) {
        throw(Error(status));
    }
    // if the new group is empty
    if (newGroup == MPI_GROUP_EMPTY) {
        // return the empty singleton
        return Group::empty;
    }
    // otherwise, wrap the new handle and return it
    return new Group(newGroup);
}


// build a group from the intersection of two others
pyre::mpi::Group *
pyre::mpi::groupIntersection(const pyre::mpi::Group * a, const pyre::mpi::Group * b) {
    // the new group
    MPI_Group newGroup;
    int status = MPI_Group_intersection(a->handle(), b->handle(), &newGroup);
    // if the MPI call failed
    if (status != MPI_SUCCESS) {
        throw(Error(status));
    }
    // if the new group is empty
    if (newGroup == MPI_GROUP_EMPTY) {
        // return the empty singleton
        return Group::empty;
    }
    // otherwise, wrap the new handle and return it
    return new Group(newGroup);
}


// build a group from the difference of two others
pyre::mpi::Group *
pyre::mpi::groupDifference(const pyre::mpi::Group * a, const pyre::mpi::Group * b) {
    // the new group
    MPI_Group newGroup;
    int status = MPI_Group_difference(a->handle(), b->handle(), &newGroup);
    // if the MPI call failed
    if (status != MPI_SUCCESS) {
        throw(Error(status));
    }
    // if the new group is empty
    if (newGroup == MPI_GROUP_EMPTY) {
        // return the empty singleton
        return Group::empty;
    }
    // otherwise, wrap the new handle and return it
    return new Group(newGroup);
}

// destructor
pyre::mpi::Group::~Group() throw() {
    MPI_Group_free(&_group);
}


// static data
pyre::mpi::Group * pyre::mpi::Group::null = new pyre::mpi::Group(MPI_GROUP_NULL);
pyre::mpi::Group * pyre::mpi::Group::empty = new pyre::mpi::Group(MPI_GROUP_EMPTY);


// end of file
    
