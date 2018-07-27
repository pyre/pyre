// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//


#include <portinfo>
#include <Python.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_statistics.h>

// local includes
#include "stats.h"
#include "capsules.h"


// stats::correlation
const char * const gsl::stats::correlation__name__ = "stats_correlation";
const char * const gsl::stats::correlation__doc__ = "Pearson correlation coefficient between the datasets";

PyObject *
gsl::stats::correlation(PyObject *, PyObject * args) {
    // the arguments
    PyObject * v1c;
    PyObject * v2c;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:stats_correlation",
                                  &PyCapsule_Type, &v1c, &PyCapsule_Type, &v2c);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(v1c, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a vector");
        return 0;
    }
    if (!PyCapsule_IsValid(v2c, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the second argument must be a vector");
        return 0;
    }

    // get the two vectors
    gsl_vector * v1 = static_cast<gsl_vector *>(PyCapsule_GetPointer(v1c, gsl::vector::capsule_t));
    gsl_vector * v2 = static_cast<gsl_vector *>(PyCapsule_GetPointer(v2c, gsl::vector::capsule_t));
    // the result
    double result;
    // compute the dot product
    result = gsl_stats_correlation(v1->data, 1, v2->data, 1, v1->size);
    // and return the result
    return PyFloat_FromDouble(result);
}

// s
// stats::covariance
const char * const gsl::stats::covariance__name__ = "stats_covariance";
const char * const gsl::stats::covariance__doc__ = "the covariance of two datasets";

PyObject *
gsl::stats::covariance(PyObject *, PyObject * args) {
    // the arguments
    PyObject * v1c;
    PyObject * v2c;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:stats_correlation",
                                  &PyCapsule_Type, &v1c, &PyCapsule_Type, &v2c);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(v1c, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a vector");
        return 0;
    }
    if (!PyCapsule_IsValid(v2c, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the second argument must be a vector");
        return 0;
    }

    // get the two vectors
    gsl_vector * v1 = static_cast<gsl_vector *>(PyCapsule_GetPointer(v1c, gsl::vector::capsule_t));
    gsl_vector * v2 = static_cast<gsl_vector *>(PyCapsule_GetPointer(v2c, gsl::vector::capsule_t));
    // the result
    double result;
    // compute the dot product
    result = gsl_stats_covariance(v1->data, 1, v2->data, 1, v1->size);
    // and return the result
    return PyFloat_FromDouble(result);
}

// end of file
