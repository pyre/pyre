// -*- C++ -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_extensions_mpi_communicators_h_)
#define pyre_extensions_mpi_communicators_h_


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace mpi {

            // create a communicator (MPI_Comm_create)
            extern const char * const communicatorCreate__name__;
            extern const char * const communicatorCreate__doc__;
            PyObject * communicatorCreate(PyObject *, PyObject *);

            // return the communicator size (MPI_Comm_size)
            extern const char * const communicatorSize__name__;
            extern const char * const communicatorSize__doc__;
            PyObject * communicatorSize(PyObject *, PyObject *);

            // return the process rank in a given communicator (MPI_Comm_rank)
            extern const char * const communicatorRank__name__;
            extern const char * const communicatorRank__doc__;
            PyObject * communicatorRank(PyObject *, PyObject *);

            // set a communicator barrier (MPI_Barrier)
            extern const char * const communicatorBarrier__name__;
            extern const char * const communicatorBarrier__doc__;
            PyObject * communicatorBarrier(PyObject *, PyObject *);

            // create a cartesian communicator (MPI_Cart_create)
            extern const char * const communicatorCreateCartesian__name__;
            extern const char * const communicatorCreateCartesian__doc__;
            PyObject * communicatorCreateCartesian(PyObject *, PyObject *);

            // return the coordinates of the process in the cartesian communicator (MPI_Cart_coords)
            extern const char * const communicatorCartesianCoordinates__name__;
            extern const char * const communicatorCartesianCoordinates__doc__;
            PyObject * communicatorCartesianCoordinates(PyObject *, PyObject *);

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
