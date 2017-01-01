// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// code guard
#if !defined(pyre_mpi_Communicator_h)
#define pyre_mpi_Communicator_h

// place Communicator in namespace pyre::mpi
namespace pyre {
    namespace mpi {
        class Communicator;
        class Error;
        class Group;
    }
}

// declaration
class pyre::mpi::Communicator {
    friend class Shareable<Communicator>;

    // types
public:
    typedef MPI_Comm handle_t;
    typedef Handle<Communicator> storage_t;
    typedef Shareable<Communicator> shared_t;

    typedef Group group_t;
    typedef Communicator communicator_t;
    typedef std::vector<int> ranklist_t;

    // interface
public:
    inline handle_t handle() const throw();
    inline bool isNull() const throw();

    inline void barrier() const throw(Error); // build a synchronization barrier

    inline int rank() const throw(Error); // compute the rank of this process
    inline int size() const throw(Error); // compute my size

    inline group_t group() const throw(Error); // access to my group of processes
    inline communicator_t communicator(const group_t &) const throw(Error);

    inline communicator_t cartesian(const ranklist_t &, const ranklist_t &, int) const throw(Error);
    inline ranklist_t coordinates(int) const throw(Error);

    // meta methods
public:
    inline ~Communicator() throw();
    inline Communicator(handle_t, bool = false) throw();
    inline Communicator(const Communicator &) throw();
    inline const Communicator & operator=(const Communicator &) throw();

    // hidden
private:
    static inline void free(MPI_Comm *) throw(Error);

    // data members
private:
    storage_t _handle;
};


// get the inline definitions
#define pyre_mpi_Communicator_icc
#include "Communicator.icc"
#undef pyre_mpi_Communicator_icc


# endif
// end of file
