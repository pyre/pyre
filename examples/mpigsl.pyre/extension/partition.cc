// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// my declarations
#include "partition.h"

// the external libraries
#include <mpi.h>
#include <gsl/gsl_matrix.h>
// the pyre mpi library
#include <pyre/mpi.h>
// the extension info
#include <pyre/gsl/capsules.h>
#include <pyre/mpi/capsules.h>


// gather
const char * const
mpigsl::
gather__name__ = "gather";

const char * const
mpigsl::
gather__doc__ = "gather a matrix from the members of a communicator";

PyObject * 
mpigsl::
gather(PyObject *, PyObject *)
{
    Py_INCREF(Py_None);
    return Py_None;
}
    

// scatter
const char * const
mpigsl::
scatter__name__ = "scatter";

const char * const 
mpigsl::
scatter__doc__ = "scatter a matrix to the members of a communicator";

PyObject * 
mpigsl::
scatter(PyObject *, PyObject * args)
{
    // place holders 
    int source, rows, columns;
    PyObject *communicatorCapsule, *matrixCapsule;

    // parse the argument list
    if (!PyArg_ParseTuple(
                          args,
                          "O!iO(ii):scatter",
                          &PyCapsule_Type, &communicatorCapsule,
                          &source,
                          &matrixCapsule, // don't force the capsule type check; it may be {None}
                          &rows, &columns
                          )) {
        return 0;
    }
    // check the communicator capsule
    if (!PyCapsule_IsValid(communicatorCapsule, mpi::communicator::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }
    // get the communicator
    pyre::mpi::communicator_t * comm = 
        static_cast<pyre::mpi::communicator_t *>
        (PyCapsule_GetPointer(communicatorCapsule, mpi::communicator::capsule_t));

    // the pointer to source payload
    double * data = 0;
    // I only have a valid matrix at the {source} rank
    if (comm->rank() == source) {
        // check the matrix capsule
        if (!PyCapsule_IsValid(matrixCapsule, gsl::matrix::capsule_t)) {
            PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for source");
            return 0;
        }
        // get the source matrix
        gsl_matrix * matrix =
            static_cast<gsl_matrix *>
            (PyCapsule_GetPointer(matrixCapsule, gsl::matrix::capsule_t));
        // and extract the pointer to the payload
        data = matrix->data;
    }

    // build the destination matrix
    gsl_matrix * destination = gsl_matrix_alloc(rows, columns);

    // scatter the data
    int status = MPI_Scatter(
                             data, rows*columns, MPI_DOUBLE,
                             destination->data, rows*columns, MPI_DOUBLE,
                             source, comm->handle()
                             );
    
    // wrap the destination matrix in a capsule and return it
    return PyCapsule_New(destination, gsl::matrix::capsule_t, gsl::matrix::free);
}

    
// end of file
