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

class pyre::mpi::Communicator {
// interface
public:
    int size() const;
    int rank() const;

    void barrier() const;
    void cartesianCoordinates(int rank, int dim, int * coordinates) const;

    MPI_Comm handle() const;

    // factories
    Communicator * newCommunicator(const Group & group) const;
    Communicator * cartesian(int size, int * procs, int * periods, int reorder) const;


// meta-methods
public:
    Communicator(MPI_Comm handle);
    virtual ~Communicator();

// hide these
private:
    Communicator(const Communicator &);
    Communicator & operator=(const Communicator &);

// instance atributes
protected:

    MPI_Comm _communicator;
};

#endif

// end of file
