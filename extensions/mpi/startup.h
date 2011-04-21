// -*- C++ -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#if !defined(pyre_extensions_mpi_startup_h)
#define pyre_extensions_mpi_startup_h

// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace mpi {
            // create a communicator group (MPI_Comm_group)
            extern const char * const initialize__name__;
            extern const char * const initialize__doc__;
            PyObject * initialize(PyObject *, PyObject *);

            // return the communicator group size (MPI_Group_size)
            extern const char * const finalize__name__;
            extern const char * const finalize__doc__;
            PyObject * finalize(PyObject *, PyObject *);

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
