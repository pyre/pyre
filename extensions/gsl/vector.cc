// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <gsl/gsl_vector.h>
#include <iostream>

#include "vector.h"


// local
static void free(PyObject *);
static const char * capsule_t = "gsl.vector";


// construction
const char * const gsl::vector::allocate__name__ = "vector_allocate";
const char * const gsl::vector::allocate__doc__ = "allocate a vector";

PyObject * 
gsl::vector::allocate(PyObject *, PyObject * args) {
    // place holders for the python arguments
    size_t length;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "l:vector_allocate", &length);
    // if something went wrong
    if (!status) return 0;

    // allocate a vector
    gsl_vector * v = gsl_vector_alloc(length);
    std::cout << " gsl.vector_allocate: vector@" << v << ", size=" << length << std::endl;

    // wrap it in a capsule and return it
    return PyCapsule_New(v, capsule_t, free);
}


// initialization
const char * const gsl::vector::set_zero__name__ = "vector_set_zero";
const char * const gsl::vector::set_zero__doc__ = "zero out the elements of a vector";

PyObject * 
gsl::vector::set_zero(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    std::cout << " gsl.vector_set_zero: vector@" << v << std::endl;
    // zero it out
    gsl_vector_set_zero(v);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// destructor
void free(PyObject * capsule)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) return;
    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    std::cout << " gsl.vector_free: vector@" << v << std::endl;
    // deallocate
    gsl_vector_free(v);
    // and return
    return;
}


// end of file
