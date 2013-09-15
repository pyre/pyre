// -*- C++ -*-
// 
// michael a.g. aïvázis
// orthologue
// (c) 1998-2013 all rights reserved
// 

// code guard
#if !defined(pyre_mpi_Group_h)
#define pyre_mpi_Group_h

// place Group in namespace pyre::mpi
namespace pyre {
    namespace mpi {
        class Group;
        class Communicator;

        inline Group groupUnion(const Group &, const Group &) throw(Error);
        inline Group groupIntersection(const Group &, const Group &) throw(Error);
        inline Group groupDifference(const Group &, const Group &) throw(Error);
    }
}

// declaration
class pyre::mpi::Group {
    friend class Communicator;
    friend class Shareable<Group>;

    friend Group groupUnion(const Group &, const Group &) throw(Error);
    friend Group groupIntersection(const Group &, const Group &) throw(Error);
    friend Group groupDifference(const Group &, const Group &) throw(Error);

    // types
public:
    typedef MPI_Group handle_t;
    typedef Handle<Group> storage_t;
    typedef Shareable<Group> shared_t;

    typedef Group group_t;
    typedef std::vector<int> ranklist_t;

    // interface
public:
    inline bool isEmpty() const throw();
    inline int rank() const throw(Error);
    inline int size() const throw(Error);

    inline group_t include(const ranklist_t &) const throw(Error);
    inline group_t exclude(const ranklist_t &) const throw(Error);

    // meta methods
public:
    inline ~Group() throw();
    inline Group(handle_t handle, bool = false) throw();
    inline Group(const Group &) throw();
    inline const Group & operator=(const Group &) throw();

    // hidden
private:
    inline operator handle_t () const throw();
    static inline void free(MPI_Group *) throw(Error);
    
    // data members
private:
    storage_t _handle;
};


// get the inline definitions
#define pyre_mpi_Group_icc
#include "Group.icc"
#undef pyre_mpi_Group_icc


# endif
// end of file
