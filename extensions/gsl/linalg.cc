// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 


#include <portinfo>
#include <Python.h>
#include <map>
// turn on GSL inlining
#define HAVE_INLINE
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>

// local includes
#include "linalg.h"
#include "capsules.h"


// linalg::cholesky_decomp
const char * const gsl::linalg::cholesky_decomp__name__ = "linalg_cholesky_decomp";
const char * const gsl::linalg::cholesky_decomp__doc__ = "compute the scalar product of two vectors";

PyObject * 
gsl::linalg::cholesky_decomp(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:linalg_cholesky_decomp", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(capsule, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the argument must be a matrix");
        return 0;
    }
    // get the matrix
    gsl_matrix * m = 
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, gsl::matrix::capsule_t));
    // compute the decomposition
    gsl_linalg_cholesky_decomp(m);
    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// end of file
