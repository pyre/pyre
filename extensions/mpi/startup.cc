// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// configuration option
#include <portinfo>
// python api
#include <Python.h>
// journal
#include <pyre/journal.h>
// my wrappers over the mpi api
#include <pyre/mpi.h>
// my local declarations
#include "startup.h"


// initialize
const char * const mpi::initialize__name__ = "init";
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
    pyre::journal::debug_t channel("mpi.init");
    // and if the use cares
    if (channel) {
        // get the world communicator layout
        int rank, size;
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);
        // and show
        channel
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
    // check whether MPI is already initialized
    int isInitialized = 0;
    int status = MPI_Initialized(&isInitialized);

    // if something went wrong
    if (status != MPI_SUCCESS) {
        // bail
        Py_INCREF(Py_None);
        return Py_None;
    }

    // check whether MPI is already finalized
    int isFinalized = 0;
    status = MPI_Finalized(&isFinalized);

    // if something went wrong
    if (status != MPI_SUCCESS) {
        // also bail
        Py_INCREF(Py_None);
        return Py_None;
    }

    // if all is good and mpi has been initialized previously
    if (isInitialized && !isFinalized) {
        // get the world communicator layout
        int rank, size;
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);
        // shut down mpi
        int success = MPI_Finalize();

        // build a channel
        pyre::journal::debug_t channel("mpi.init");
        // if the user cares
        if (channel) {
            // indicate that mpi is down
            channel
                << pyre::journal::at(__HERE__)
                << "[" << rank << ":" << size << "] " << "finalized mpi; status = " << success
                << pyre::journal::endl;
        }
    }

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
