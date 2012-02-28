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
#include <gsl/gsl_randist.h>

#include "pdf.h"
#include "capsules.h"


// uniform::sample
const char * const gsl::pdf::uniform::sample__name__ = "uniform_sample";
const char * const gsl::pdf::uniform::sample__doc__ = 
    "return a sample from the uniform distribution";

PyObject * 
gsl::pdf::uniform::sample(PyObject *, PyObject * args) {
    // the arguments
    double a, b;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "(dd)O!:uniform_sample",
                                  &a, &b, &PyCapsule_Type, &capsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // get the rng
    gsl_rng * r = static_cast<gsl_rng *>(PyCapsule_GetPointer(capsule, gsl::rng::capsule_t));
    // sample the distribution and return the value
    return PyFloat_FromDouble(gsl_ran_flat(r, a, b));
}


// uniform::density
const char * const gsl::pdf::uniform::density__name__ = "uniform_density";
const char * const gsl::pdf::uniform::density__doc__ = "return the uniform distribution density";

PyObject * 
gsl::pdf::uniform::density(PyObject *, PyObject * args) {
    // the arguments
    double x, a, b;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "(dd)d:uniform_density", &a, &b, &x);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // compute the density and return the value
    return PyFloat_FromDouble(gsl_ran_flat_pdf(x, a, b));
}


// gaussian::sample
const char * const gsl::pdf::gaussian::sample__name__ = "gaussian_sample";
const char * const gsl::pdf::gaussian::sample__doc__ = 
    "return a sample from the gaussian distribution";

PyObject * 
gsl::pdf::gaussian::sample(PyObject *, PyObject * args) {
    // the arguments
    double sigma;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "dO!:gaussian_sample",
                                  &sigma, &PyCapsule_Type, &capsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // get the rng
    gsl_rng * r = static_cast<gsl_rng *>(PyCapsule_GetPointer(capsule, gsl::rng::capsule_t));
    // sample the distribution and return the value
    return PyFloat_FromDouble(gsl_ran_gaussian(r, sigma));
}


// gaussian::density
const char * const gsl::pdf::gaussian::density__name__ = "gaussian_density";
const char * const gsl::pdf::gaussian::density__doc__ = "return the gaussian distribution density";

PyObject * 
gsl::pdf::gaussian::density(PyObject *, PyObject * args) {
    // the arguments
    double x, sigma;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "dd:gaussian_density", &sigma, &x);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // compute the density and return the value
    return PyFloat_FromDouble(gsl_ran_gaussian_pdf(x, sigma));
}


// end of file
