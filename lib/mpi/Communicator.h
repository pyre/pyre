// -*- C++ -*-
//
// michael a.g. aivazis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#if !defined(pyre_mpi_Communicator_h__)
#define pyre_mpi_Communicator_h__

namespace pyre {
    namespace mpi {
        class Group;
        class Communicator;
    }
}

// encapsulation of MPI_Comm
class pyre::mpi::Communicator {
// interface
public:
    inline int size() const throw(Error);
    inline int rank() const throw(Error);
    inline MPI_Comm handle() const throw();

    inline void barrier() const throw(Error);
    void cartesianCoordinates(int rank, int dim, int * coordinates) const;

    // factories
    // make a communicator out of the given group of processes
    Communicator * newCommunicator(const Group & group) const;
    // build a Cartesian communicator
    Communicator * cartesian(int size, int * procs, int * periods, int reorder) const;

// meta-methods
public:
    inline Communicator(MPI_Comm handle) throw();
    virtual ~Communicator() throw();

// hide these
private:
    Communicator(const Communicator &);
    Communicator & operator=(const Communicator &);

// data
public:
    static Communicator * world; // a wrapper around MPI_COMM_WORLD

// instance atributes
protected:
    MPI_Comm _communicator;
};

// get the inline definitions
#define pyre_mpi_Communicator_icc
#include "Communicator.icc"
#undef pyre_mpi_Communicator_icc

#endif

// end of file
