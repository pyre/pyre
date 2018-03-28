// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
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

    // if anything went wrong
    if (status != MPI_SUCCESS) {
        // build an import error
        PyErr_SetString(PyExc_ImportError, "error while check mpi initialization state");
        // and raise it
        return 0;
    }

    // if all went well and mpi is not already initialized
    if (!isInitialized) {
        // do it; no need to hunt down {argc, argv}: {mpirun} does all the work
        MPI_Init(0, 0);
    }

    // build a channel
    pyre::journal::debug_t info("mpi.init");
    // and if the use cares
    if (info.isActive()) {
        // get the world communicator layout
        int rank, size;
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);
        // and show
        info
            << pyre::journal::at(__HERE__)
            << "[" << rank << ":" << size << "] " << "mpi initialized successfully"
            << pyre::journal::endl;
    }

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

    // if all is good and mpi has been initialized previously
    if (status == MPI_SUCCESS && isInitialized) {
        // shut it down
        MPI_Finalize();
    }

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
