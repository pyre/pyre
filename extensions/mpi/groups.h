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

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
