// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2013 all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <pyre/mpi.h>

#include <pyre/journal.h>

#include "startup.h"


// initialize
const char * const mpi::initialize__name__ = "initialize";
const char * const mpi::initialize__doc__ = "initialize MPI";

PyObject * mpi::initialize(PyObject *, PyObject *)
{
    // check whether MPI is already intialized
    int isInitialized = 0;
    int status = MPI_Initialized(&isInitialized);

    if (status != MPI_SUCCESS) {
        PyErr_SetString(PyExc_ImportError, "MPI_Initialized failed");
        return 0;
    }

    // allow threads
    Py_BEGIN_ALLOW_THREADS;

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

    // disallow threads
    Py_END_ALLOW_THREADS;

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}

// finalize
const char * const mpi::finalize__name__ = "finalize";
const char * const mpi::finalize__doc__ = "shut down MPI";

PyObject * mpi::finalize(PyObject *, PyObject *)
{
    // check whether MPI is already intialized
    int isInitialized = 0;
    int status = MPI_Initialized(&isInitialized);

    if (status != MPI_SUCCESS) {
        PyErr_SetString(PyExc_ImportError, "MPI_Initialized failed");
        return 0;
    }

    // if it is already initialized
    if (isInitialized) {
        // allow threads
        Py_BEGIN_ALLOW_THREADS;
        // shut it down
        MPI_Finalize();
        // disallow threads
        Py_END_ALLOW_THREADS;
    }

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
