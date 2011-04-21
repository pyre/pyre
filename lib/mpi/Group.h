// -*- C++ -*-
//
// michael a.g. aivazis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#if !defined(pyre_mpi_Group_h__)
#define pyre_mpi_Group_h__

namespace pyre {
    namespace mpi {
        class Group;
        class Communicator;
    }
}


class pyre::mpi::Group {

// interface
public:
    int size() const;
    int rank() const;
    MPI_Group handle() const;

    // factories
    static Group * newGroup(const Communicator & comm);

    Group * include(int size, int ranks[]) const;
    Group * exclude(int size, int ranks[]) const;
    
// meta-methods
public:
    Group(MPI_Group handle);
    virtual ~Group();

// hide these
private:
        
    Group(const Group &);
    Group & operator=(const Group &);

// data
protected:

    MPI_Group _group;
};


#endif

// end of file
