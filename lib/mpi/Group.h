// -*- C++ -*-
//
// michael a.g. aivazis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#if !defined(pyre_mpi_Group_h__)
#define pyre_mpi_Group_h__


// forward declarations
namespace pyre {
    namespace mpi {
        class Group;
        class Error;
        class Communicator;

        // global operators
        Group * groupUnion(const Group *, const Group *);
        Group * groupIntersection(const Group *, const Group *);
        Group * groupDifference(const Group *, const Group *);
    }
}


// a wrapper around MPI_Group
class pyre::mpi::Group {

// interface
public:
    inline int size() const throw(Error); // the size of the group
    inline int rank() const throw(Error); // the rank of this process in this group
    inline MPI_Group handle() const throw(); // access to the raw MPI handle

    // factories
    // make a group out of the processes in the given communicator
    static Group * newGroup(const Communicator & comm);
    // make a new group by including or excluding certain processes from this group
    Group * include(int size, int ranks[]) const;
    Group * exclude(int size, int ranks[]) const;
    
// meta-methods
public:
    inline Group(MPI_Group handle) throw();
    virtual ~Group();

// hide these
private:
    Group(const Group &);
    Group & operator=(const Group &);

// data
public:
    static Group * null; // a wrapper around the predefined null group
    static Group * empty; // a wrapper around the predefined empty group

protected:
    MPI_Group _group; // the raw MPI handle
};

// get the inline definitions
#define pyre_mpi_Group_icc
#include "Group.icc"
#undef pyre_mpi_Group_icc

#endif

// end of file
