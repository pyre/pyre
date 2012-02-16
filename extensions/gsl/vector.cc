// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 


#include <portinfo>
#include <Python.h>

// turn on GSL inlining
#define HAVE_INLINE
#include <gsl/gsl_vector.h>
#include "vector.h"

#include <iostream>

// local
static void free(PyObject *);
static const char * capsule_t = "gsl.vector";


// construction
const char * const gsl::vector::allocate__name__ = "vector_allocate";
const char * const gsl::vector::allocate__doc__ = "allocate a vector";

PyObject * 
gsl::vector::allocate(PyObject *, PyObject * args) {
    // place holders for the python arguments
    size_t shape;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "k:vector_allocate", &shape);
    // if something went wrong
    if (!status) return 0;

    // allocate a vector
    gsl_vector * v = gsl_vector_alloc(shape);
    // std::cout << " gsl.vector_allocate: vector@" << v << ", size=" << shape << std::endl;

    // wrap it in a capsule and return it
    return PyCapsule_New(v, capsule_t, free);
}


// initialization
const char * const gsl::vector::zero__name__ = "vector_zero";
const char * const gsl::vector::zero__doc__ = "zero out the elements of a vector";

PyObject * 
gsl::vector::zero(PyObject *, PyObject * args) {
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
    // std::cout << " gsl.vector_zero: vector@" << v << std::endl;
    // zero it out
    gsl_vector_set_zero(v);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::fill__name__ = "vector_fill";
const char * const gsl::vector::fill__doc__ = "set all elements of a vector to a value";

PyObject * 
gsl::vector::fill(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!d", &PyCapsule_Type, &capsule, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout << " gsl.vector_fill: vector@" << v << ", value=" << value << std::endl;
    // fill it out
    gsl_vector_set_all(v, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::basis__name__ = "vector_basis";
const char * const gsl::vector::basis__doc__ = "build a basis vector";

PyObject * 
gsl::vector::basis(PyObject *, PyObject * args) {
    // the arguments
    size_t index;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!k", &PyCapsule_Type, &capsule, &index);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout << " gsl.vector_basis: vector@" << v << ", index=" << index << std::endl;
    // fill it out
    gsl_vector_set_basis(v, index);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// access
const char * const gsl::vector::get__name__ = "vector_get";
const char * const gsl::vector::get__doc__ = "get the value of a vector element";

PyObject * 
gsl::vector::get(PyObject *, PyObject * args) {
    // the arguments
    size_t index;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!k", &PyCapsule_Type, &capsule, &index);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    // get the value
    double value = gsl_vector_get(v, index);
    // std::cout
        // << " gsl.vector_get: vector@" << v << ", index=" << index << ", value=" << value 
        // << std::endl;

    // return the value
    return PyFloat_FromDouble(value);
}


const char * const gsl::vector::set__name__ = "vector_set";
const char * const gsl::vector::set__doc__ = "set the value of a vector element";

PyObject * 
gsl::vector::set(PyObject *, PyObject * args) {
    // the arguments
    size_t index;
    double value;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!kd", &PyCapsule_Type, &capsule, &index, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout
        // << " gsl.vector_set: vector@" << v << ", index=" << index << ", value=" << value 
        // << std::endl;
    // set the value
    gsl_vector_set(v, index, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::contains__name__ = "vector_contains";
const char * const gsl::vector::contains__doc__ = "check whether a given value appears in vector";

PyObject * 
gsl::vector::contains(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!d", &PyCapsule_Type, &capsule, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout
        // << " gsl.vector_contains: vector@" << v << ", index=" << index << ", value=" << value 
        // << std::endl;

    // the answer
    PyObject * result = Py_False;

    // loop over the elements
    for (size_t index=0; index < v->size; index++) {
        // if i have a match
        if (value == gsl_vector_get(v, index)) {
            // update the answer
            result = Py_True;
            // and bail
            break;
        }
    }

    // return the answer
    Py_INCREF(result);
    return result;
}


// minima and maxima
const char * const gsl::vector::max__name__ = "vector_max";
const char * const gsl::vector::max__doc__ = "find the largest value contained";

PyObject * 
gsl::vector::max(PyObject *, PyObject * args) {
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
    double value = gsl_vector_max(v);
    // std::cout << " gsl.vector_max: vector@" << v << ", value=" << value << std::endl;

    // return the value
    return PyFloat_FromDouble(value);
}


const char * const gsl::vector::min__name__ = "vector_min";
const char * const gsl::vector::min__doc__ = "find the smallest value contained";

PyObject * 
gsl::vector::min(PyObject *, PyObject * args) {
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
    double value = gsl_vector_min(v);
    // std::cout << " gsl.vector_max: vector@" << v << ", value=" << value << std::endl;

    // return the value
    return PyFloat_FromDouble(value);
}


const char * const gsl::vector::minmax__name__ = "vector_minmax";
const char * const gsl::vector::minmax__doc__ = 
    "find both the smallest and the largest value contained";

PyObject * 
gsl::vector::minmax(PyObject *, PyObject * args) {
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
    double small, large;
    gsl_vector_minmax(v, &small, &large);
    // std::cout 
        // << " gsl.vector_max: vector@" << v << ", min=" << small << ", max=" << large 
        // << std::endl;

    // build the answer
    PyObject * answer = PyTuple_New(2);
    PyTuple_SET_ITEM(answer, 0, PyFloat_FromDouble(small));
    PyTuple_SET_ITEM(answer, 1, PyFloat_FromDouble(large));
    // and return
    return answer;
}


// in-place operations
const char * const gsl::vector::add__name__ = "vector_add";
const char * const gsl::vector::add__doc__ = "in-place addition of two vectors";

PyObject * 
gsl::vector::add(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!O!", &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the two vectors
    gsl_vector * v1 = static_cast<gsl_vector *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_vector * v2 = static_cast<gsl_vector *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.vector_add: vector@" << v1 << ", vector@" << v2 << std::endl;
    // perform the addition
    gsl_vector_add(v1, v2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::sub__name__ = "vector_sub";
const char * const gsl::vector::sub__doc__ = "in-place subtraction of two vectors";

PyObject * 
gsl::vector::sub(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!O!", &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the two vectors
    gsl_vector * v1 = static_cast<gsl_vector *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_vector * v2 = static_cast<gsl_vector *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.vector_sub: vector@" << v1 << ", vector@" << v2 << std::endl;
    // perform the subtraction
    gsl_vector_sub(v1, v2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::mul__name__ = "vector_mul";
const char * const gsl::vector::mul__doc__ = "in-place multiplication of two vectors";

PyObject * 
gsl::vector::mul(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!O!", &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the two vectors
    gsl_vector * v1 = static_cast<gsl_vector *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_vector * v2 = static_cast<gsl_vector *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.vector_mul: vector@" << v1 << ", vector@" << v2 << std::endl;
    // perform the multiplication
    gsl_vector_mul(v1, v2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::div__name__ = "vector_div";
const char * const gsl::vector::div__doc__ = "in-place division of two vectors";

PyObject * 
gsl::vector::div(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!O!", &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the two vectors
    gsl_vector * v1 = static_cast<gsl_vector *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_vector * v2 = static_cast<gsl_vector *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.vector_div: vector@" << v1 << ", vector@" << v2 << std::endl;
    // perform the division
    gsl_vector_div(v1, v2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::shift__name__ = "vector_shift";
const char * const gsl::vector::shift__doc__ = "in-place addition of a constant to a vector";

PyObject * 
gsl::vector::shift(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * self;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!d", &PyCapsule_Type, &self, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the two vectors
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(self, capsule_t));
    // std::cout << " gsl.vector_shift: vector@" << v << ", value=" << value << std::endl;
    // perform the shift
    gsl_vector_add_constant(v, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::vector::scale__name__ = "vector_scale";
const char * const gsl::vector::scale__doc__ = "in-place scaling of a vector by a constant";

PyObject * 
gsl::vector::scale(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * self;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!d", &PyCapsule_Type, &self, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the two vectors
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(self, capsule_t));
    // std::cout << " gsl.vector_scale: vector@" << v << ", value=" << value << std::endl;
    // perform the scale
    gsl_vector_scale(v, value);

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
    // std::cout << " gsl.vector_free: vector@" << v << std::endl;
    // deallocate
    gsl_vector_free(v);
    // and return
    return;
}


// end of file
