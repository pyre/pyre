// -*- C++ -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#if !defined(pyre_extensions_mpi_groups_h)
#define pyre_extensions_mpi_groups_h

// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace mpi {

            // the predefined groups
            extern PyObject * nullGroup;
            extern PyObject * emptyGroup;

            // the group capsule destructor
            void deleteGroup(PyObject *);

            // check whether a group is empty
            extern const char * const groupIsEmpty__name__;
            extern const char * const groupIsEmpty__doc__;
            PyObject * groupIsEmpty(PyObject *, PyObject *);

            // create a communicator group (MPI_Comm_group)
            extern const char * const groupCreate__name__;
            extern const char * const groupCreate__doc__;
            PyObject * groupCreate(PyObject *, PyObject *);

            // return the communicator group size (MPI_Group_size)
            extern const char * const groupSize__name__;
            extern const char * const groupSize__doc__;
            PyObject * groupSize(PyObject *, PyObject *);

            // return the process rank in a given communicator group (MPI_Group_rank)
            extern const char * const groupRank__name__;
            extern const char * const groupRank__doc__;
            PyObject * groupRank(PyObject *, PyObject *);

            // return the process rank in a given communicator group (MPI_Group_incl)
            extern const char * const groupInclude__name__;
            extern const char * const groupInclude__doc__;
            PyObject * groupInclude(PyObject *, PyObject *);

            // return the process rank in a given communicator group (MPI_Group_excl)
            extern const char * const groupExclude__name__;
            extern const char * const groupExclude__doc__;
            PyObject * groupExclude(PyObject *, PyObject *);

            // build a group out of the union of two others
            extern const char * const groupUnion__name__;
            extern const char * const groupUnion__doc__;
            PyObject * groupUnion(PyObject *, PyObject *);

            // build a group out of the intersection of two others
            extern const char * const groupIntersection__name__;
            extern const char * const groupIntersection__doc__;
            PyObject * groupIntersection(PyObject *, PyObject *);

            // build a group out of the difference of two others
            extern const char * const groupDifference__name__;
            extern const char * const groupDifference__doc__;
            PyObject * groupDifference(PyObject *, PyObject *);

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
