// -*- C++ -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <pyre/mpi.h>

#include <pyre/journal.h>

#include "startup.h"


// initialize
const char * const 
pyre::extensions::mpi::
initialize__name__ = "initialize";

const char * const 
pyre::extensions::mpi::
initialize__doc__ = "initialize MPI";

PyObject *
pyre::extensions::mpi::
initialize(PyObject *, PyObject *)
{
    // check whether MPI is already intialized
    int isInitialized = 0;
    int status = MPI_Initialized(&isInitialized);

    if (status != MPI_SUCCESS) {
        PyErr_SetString(PyExc_ImportError, "MPI_Initialized failed");
        return 0;
    }

    if (!isInitialized) {
        MPI_Init(0, 0);
    }

    pyre::journal::debug_t info("mpi.init");
    if (info.isActive()) {
        int rank, size;
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);

        info
            << pyre::journal::at(__HERE__)
            << "[" << rank << ":" << size << "] "
            << "MPI_Init succeeded"
            << pyre::journal::endl;
    }

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}

// finalize
const char * const
pyre::extensions::mpi::
 finalize__name__ = "finalize";

const char * const 
pyre::extensions::mpi::
finalize__doc__ = "shut down MPI";

PyObject *
pyre::extensions::mpi::
finalize(PyObject *, PyObject *)
{
    // check whether MPI is already intialized
    int isInitialized = 0;
    int status = MPI_Initialized(&isInitialized);

    if (status != MPI_SUCCESS) {
        PyErr_SetString(PyExc_ImportError, "MPI_Initialized failed");
        return false;
    }

    /// shut it down
    if (isInitialized) {
        MPI_Finalize();
    }

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
