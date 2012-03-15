// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 


#include <portinfo>
#include <Python.h>
#include <sstream>

#include <gsl/gsl_matrix.h>
#include "matrix.h"
#include "capsules.h"


// construction
const char * const gsl::matrix::alloc__name__ = "matrix_alloc";
const char * const gsl::matrix::alloc__doc__ = "allocate a matrix";

PyObject * 
gsl::matrix::alloc(PyObject *, PyObject * args) {
    // place holders for the python arguments
    size_t s0, s1;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "(kk):matrix_alloc", &s0, &s1);
    // if something went wrong
    if (!status) return 0;

    // allocate a matrix
    gsl_matrix * m = gsl_matrix_alloc(s0, s1);
    // std::cout << " gsl.matrix_allocate: matrix@" << m << ", size=" << length << std::endl;

    // wrap it in a capsule and return it
    return PyCapsule_New(m, capsule_t, free);
}


// initialization
const char * const gsl::matrix::zero__name__ = "matrix_zero";
const char * const gsl::matrix::zero__doc__ = "zero out the elements of a matrix";

PyObject * 
gsl::matrix::zero(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:matrix_zero", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout << " gsl.matrix_zero: matrix@" << m << std::endl;
    // zero it out
    gsl_matrix_set_zero(m);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::matrix::fill__name__ = "matrix_fill";
const char * const gsl::matrix::fill__doc__ = "set all elements of a matrix to a value";

PyObject * 
gsl::matrix::fill(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!d:matrix_fill", &PyCapsule_Type, &capsule, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout << " gsl.matrix_fill: matrix@" << m << ", value=" << value << std::endl;
    // fill it out
    gsl_matrix_set_all(m, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// matrix_identity
const char * const gsl::matrix::identity__name__ = "matrix_identity";
const char * const gsl::matrix::identity__doc__ = "build an identity matrix";

PyObject * 
gsl::matrix::identity(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:matrix_identity", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout << " gsl.matrix_identity: matrix@" << m << ", index=" << index << std::endl;
    // fill it out
    gsl_matrix_set_identity(m);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// copy
const char * const gsl::matrix::copy__name__ = "matrix_copy";
const char * const gsl::matrix::copy__doc__ = "build a copy of a matrix";

PyObject * 
gsl::matrix::copy(PyObject *, PyObject * args) {
    // the arguments
    PyObject * sourceCapsule;
    PyObject * destinationCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:matrix_copy", 
                                  &PyCapsule_Type, &destinationCapsule,
                                  &PyCapsule_Type, &sourceCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the source capsule is not valid
    if (!PyCapsule_IsValid(sourceCapsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for source");
        return 0;
    }
    // bail out if the destination capsule is not valid
    if (!PyCapsule_IsValid(destinationCapsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for destination");
        return 0;
    }

    // get the matrices
    gsl_matrix * source =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(sourceCapsule, capsule_t));
    gsl_matrix * destination =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(destinationCapsule, capsule_t));
    // copy the data
    gsl_matrix_memcpy(destination, source);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// transpose
const char * const gsl::matrix::transpose__name__ = "matrix_transpose";
const char * const gsl::matrix::transpose__doc__ = "build a transpose of a matrix";

PyObject * 
gsl::matrix::transpose(PyObject *, PyObject * args) {
    // the arguments
    PyObject * sourceCapsule;
    PyObject * destinationCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O:matrix_transpose", 
                                  &PyCapsule_Type, &sourceCapsule,
                                  &destinationCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the source capsule is not valid
    if (!PyCapsule_IsValid(sourceCapsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for source");
        return 0;
    }
    // get the source matrix
    gsl_matrix * source =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(sourceCapsule, capsule_t));

    // check the destination object
    if (destinationCapsule == Py_None) {
        // we are doing this in place, assuming a square matrix
        gsl_matrix_transpose(source);
        // return None
        Py_INCREF(Py_None);
        return Py_None;
    }

    // otherwise, destinationCapsule must also be a valid matrix capsule
    if (
        !PyCapsule_CheckExact(destinationCapsule) ||
        !PyCapsule_IsValid(destinationCapsule, capsule_t)
        ) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for destination");
        return 0;
    }

    gsl_matrix * destination =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(destinationCapsule, capsule_t));
    // transpose the data
    gsl_matrix_transpose_memcpy(destination, source);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// access
const char * const gsl::matrix::get__name__ = "matrix_get";
const char * const gsl::matrix::get__doc__ = "get the value of a matrix element";

PyObject * 
gsl::matrix::get(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    long index1, index2;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!(ll):matrix_get",
                                  &PyCapsule_Type, &capsule, &index1, &index2);
    // bail out if something went wrong during argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));

    // reflect negative indices about the end of the matrix
    if (index1 < 0) index1 += m->size1;
    if (index2 < 0) index2 += m->size2;

    // convert to unsigned values
    size_t i1 = index1;
    size_t i2 = index2;
    // bounds check index 1
    if (i1 < 0 || i1 >= m->size1) {
        // build an error message
        std::stringstream msg;
        msg << "matrix index " << index1 << " out of range";
        // register the error
        PyErr_SetString(PyExc_IndexError, msg.str().c_str());
        // and raise the exception
        return 0;
    }
    // bounds check index 2
    if (i2 < 0 || i2 >= m->size2) {
        // build an error message
        std::stringstream msg;
        msg << "matrix index " << index2 << " out of range";
        // register the error
        PyErr_SetString(PyExc_IndexError, msg.str().c_str());
        // and raise the exception
        return 0;
    }

    // get the value
    double value = gsl_matrix_get(m, i1, i2);
    // std::cout
        // << " gsl.matrix_get: matrix@" << m << ", index=" << index << ", value=" << value 
        // << std::endl;

    // return the value
    return PyFloat_FromDouble(value);
}


const char * const gsl::matrix::set__name__ = "matrix_set";
const char * const gsl::matrix::set__doc__ = "set the value of a matrix element";

PyObject * 
gsl::matrix::set(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * capsule;
    long index1, index2;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!(ll)d:matrix_set",
                                  &PyCapsule_Type, &capsule, &index1, &index2, &value);
    // bail out if something went wrong during argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout
        // << " gsl.matrix_set: matrix@" << m << ", index=" << index << ", value=" << value 
        // << std::endl;

    // reflect negative indices about the end of the matrix
    if (index1 < 0) index1 += m->size1;
    if (index2 < 0) index2 += m->size2;

    // convert to unsigned values
    size_t i1 = index1;
    size_t i2 = index2;
    // bounds check index 1
    if (i1 < 0 || i1 >= m->size1) {
        // build an error message
        std::stringstream msg;
        msg << "matrix index " << index1 << " out of range";
        // register the error
        PyErr_SetString(PyExc_IndexError, msg.str().c_str());
        // and raise the exception
        return 0;
    }
    // bounds check index 2
    if (i2 < 0 || i2 >= m->size2) {
        // build an error message
        std::stringstream msg;
        msg << "matrix index " << index2 << " out of range";
        // register the error
        PyErr_SetString(PyExc_IndexError, msg.str().c_str());
        // and raise the exception
        return 0;
    }

    // set the value
    gsl_matrix_set(m, index1, index2, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// slicing: get_col
const char * const gsl::matrix::get_col__name__ = "matrix_get_col";
const char * const gsl::matrix::get_col__doc__ = "return a column of a matrix";

PyObject * 
gsl::matrix::get_col(PyObject *, PyObject * args) {
    // the arguments
    long index;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!l:matrix_get_col",
                                  &PyCapsule_Type, &capsule, &index);
    // bail out if something went wrong during argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));

    // reflect negative indices about the end of the matrix
    if (index < 0 ) index += m->size2;

    // convert to unsigned values
    size_t i = index;
    // bounds check index
    if (i < 0 || i >= m->size2) {
        // build an error message
        std::stringstream msg;
        msg << "matrix column index " << index << " out of range";
        // register the error
        PyErr_SetString(PyExc_IndexError, msg.str().c_str());
        // and raise the exception
        return 0;
    }

    // create a vector to hold the column
    gsl_vector * v = gsl_vector_alloc(m->size1);
    // get the column
    gsl_matrix_get_col(v, m, i);

    // wrap the column in a capsule and return it
    return PyCapsule_New(v, gsl::vector::capsule_t, gsl::vector::free);
}


// slicing: get_row
const char * const gsl::matrix::get_row__name__ = "matrix_get_row";
const char * const gsl::matrix::get_row__doc__ = "return a row of a matrix";

PyObject * 
gsl::matrix::get_row(PyObject *, PyObject * args) {
    // the arguments
    long index;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!l:matrix_get_row",
                                  &PyCapsule_Type, &capsule, &index);
    // bail out if something went wrong during argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));

    // reflect negative indices about the end of the matrix
    if (index < 0 ) index += m->size1;

    // convert to unsigned values
    size_t i = index;
    // bounds check index
    if (i < 0 || i >= m->size1) {
        // build an error message
        std::stringstream msg;
        msg << "matrix row index " << index << " out of range";
        // register the error
        PyErr_SetString(PyExc_IndexError, msg.str().c_str());
        // and raise the exception
        return 0;
    }

    // create a vector to hold the row
    gsl_vector * v = gsl_vector_alloc(m->size2);
    // get the row
    gsl_matrix_get_row(v, m, i);

    // wrap the column in a capsule and return it
    return PyCapsule_New(v, gsl::vector::capsule_t, gsl::vector::free);
}


// slicing: set_col
const char * const gsl::matrix::set_col__name__ = "matrix_set_col";
const char * const gsl::matrix::set_col__doc__ = "set a col of a matrix to the given vector";

PyObject * 
gsl::matrix::set_col(PyObject *, PyObject * args) {
    // the arguments
    size_t index;
    PyObject * capsule;
    PyObject * vCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!kO!:matrix_set_col",
                                  &PyCapsule_Type, &capsule,
                                  &index,
                                  &PyCapsule_Type, &vCapsule
                                  );
    // bail out if something went wrong during argument unpacking
    if (!status) return 0;
    // bail out if the matrix capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }
    // bail out if the vector capsule is not valid
    if (!PyCapsule_IsValid(vCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = 
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // get the vector
    gsl_vector * v = 
        static_cast<gsl_vector *>(PyCapsule_GetPointer(vCapsule, gsl::vector::capsule_t));

    // set the col
    gsl_matrix_set_col(m, index, v);

    // return
    Py_INCREF(Py_None);
    return Py_None;
}


// slicing: set_row
const char * const gsl::matrix::set_row__name__ = "matrix_set_row";
const char * const gsl::matrix::set_row__doc__ = "set a row of a matrix to the given vector";

PyObject * 
gsl::matrix::set_row(PyObject *, PyObject * args) {
    // the arguments
    size_t index;
    PyObject * capsule;
    PyObject * vCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!kO!:matrix_set_row",
                                  &PyCapsule_Type, &capsule,
                                  &index,
                                  &PyCapsule_Type, &vCapsule
                                  );
    // bail out if something went wrong during argument unpacking
    if (!status) return 0;
    // bail out if the matrix capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }
    // bail out if the vector capsule is not valid
    if (!PyCapsule_IsValid(vCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = 
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // get the vector
    gsl_vector * v = 
        static_cast<gsl_vector *>(PyCapsule_GetPointer(vCapsule, gsl::vector::capsule_t));

    // set the row
    gsl_matrix_set_row(m, index, v);

    // return
    Py_INCREF(Py_None);
    return Py_None;
}


// contains
const char * const gsl::matrix::contains__name__ = "matrix_contains";
const char * const gsl::matrix::contains__doc__ = "check whether a given value appears in matrix";

PyObject * 
gsl::matrix::contains(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!d:matrix_contains", &PyCapsule_Type, &capsule, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    // std::cout
        // << " gsl.matrix_contains: matrix@" << m << ", index=" << index << ", value=" << value 
        // << std::endl;

    // the answer
    PyObject * result = Py_False;

    // loop over the elements
    for (size_t index0=0; index0 < m->size1; index0++) {
        for (size_t index1=0; index1 < m->size2; index1++) {
            // if i have a match
            if (value == gsl_matrix_get(m, index0, index1)) {
                // update the answer
                result = Py_True;
                // and bail
                break;
            }
        }
    }

    // return the answer
    Py_INCREF(result);
    return result;
}


// minima and maxima
const char * const gsl::matrix::max__name__ = "matrix_max";
const char * const gsl::matrix::max__doc__ = "find the largest value contained";

PyObject * 
gsl::matrix::max(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:matrix_max", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    double value = gsl_matrix_max(m);
    // std::cout << " gsl.matrix_max: matrix@" << m << ", value=" << value << std::endl;

    // return the value
    return PyFloat_FromDouble(value);
}


const char * const gsl::matrix::min__name__ = "matrix_min";
const char * const gsl::matrix::min__doc__ = "find the smallest value contained";

PyObject * 
gsl::matrix::min(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:matrix_min", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    double value = gsl_matrix_min(m);
    // std::cout << " gsl.matrix_max: matrix@" << m << ", value=" << value << std::endl;

    // return the value
    return PyFloat_FromDouble(value);
}


const char * const gsl::matrix::minmax__name__ = "matrix_minmax";
const char * const gsl::matrix::minmax__doc__ = 
    "find both the smallest and the largest value contained";

PyObject * 
gsl::matrix::minmax(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:matrix_minmax", &PyCapsule_Type, &capsule);
    // if something went wrong
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the matrix
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, capsule_t));
    double small, large;
    gsl_matrix_minmax(m, &small, &large);
    // std::cout 
        // << " gsl.matrix_max: matrix@" << m << ", min=" << small << ", max=" << large 
        // << std::endl;

    // build the answer
    PyObject * answer = PyTuple_New(2);
    PyTuple_SET_ITEM(answer, 0, PyFloat_FromDouble(small));
    PyTuple_SET_ITEM(answer, 1, PyFloat_FromDouble(large));
    // and return
    return answer;
}


// equal
const char * const gsl::matrix::equal__name__ = "matrix_equal";
const char * const gsl::matrix::equal__doc__ = "check two matrices for equality";

PyObject * 
gsl::matrix::equal(PyObject *, PyObject * args) {
    // the arguments
    PyObject * leftCapsule;
    PyObject * rightCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:matrix_equal", 
                                  &PyCapsule_Type, &rightCapsule,
                                  &PyCapsule_Type, &leftCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the left capsule is not valid
    if (!PyCapsule_IsValid(leftCapsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for the left operand");
        return 0;
    }
    // bail out if the right capsule is not valid
    if (!PyCapsule_IsValid(rightCapsule, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for right operand");
        return 0;
    }

    // get the matrices
    gsl_matrix * left =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(leftCapsule, capsule_t));
    gsl_matrix * right =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(rightCapsule, capsule_t));

    // the answer
    PyObject * answer = gsl_matrix_equal(left, right) ? Py_True : Py_False;
    // return 
    Py_INCREF(answer);
    return answer;
}


// in-place operations
const char * const gsl::matrix::add__name__ = "matrix_add";
const char * const gsl::matrix::add__doc__ = "in-place addition of two matrices";

PyObject * 
gsl::matrix::add(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:matrix_add",
                                  &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the two matrices
    gsl_matrix * m1 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_matrix * m2 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.matrix_add: matrix@" << m1 << ", matrix@" << m2 << std::endl;
    // perform the addition
    gsl_matrix_add(m1, m2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::matrix::sub__name__ = "matrix_sub";
const char * const gsl::matrix::sub__doc__ = "in-place subtraction of two matrices";

PyObject * 
gsl::matrix::sub(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:matrix_sub",
                                  &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the two matrices
    gsl_matrix * m1 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_matrix * m2 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.matrix_sub: matrix@" << m1 << ", matrix@" << m2 << std::endl;
    // perform the subtraction
    gsl_matrix_sub(m1, m2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::matrix::mul__name__ = "matrix_mul";
const char * const gsl::matrix::mul__doc__ = "in-place multiplication of two matrices";

PyObject * 
gsl::matrix::mul(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:matrix_mul",
                                  &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the two matrices
    gsl_matrix * m1 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_matrix * m2 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.matrix_mul: matrix@" << m1 << ", matrix@" << m2 << std::endl;
    // perform the multiplication
    gsl_matrix_mul_elements(m1, m2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::matrix::div__name__ = "matrix_div";
const char * const gsl::matrix::div__doc__ = "in-place division of two matrices";

PyObject * 
gsl::matrix::div(PyObject *, PyObject * args) {
    // the arguments
    PyObject * self;
    PyObject * other;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:matrix_div",
                                  &PyCapsule_Type, &self, &PyCapsule_Type, &other);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t) || !PyCapsule_IsValid(other, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the two matrices
    gsl_matrix * m1 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(self, capsule_t));
    gsl_matrix * m2 = static_cast<gsl_matrix *>(PyCapsule_GetPointer(other, capsule_t));
    // std::cout << " gsl.matrix_div: matrix@" << m1 << ", matrix@" << m2 << std::endl;
    // perform the division
    gsl_matrix_div_elements(m1, m2);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::matrix::shift__name__ = "matrix_shift";
const char * const gsl::matrix::shift__doc__ = "in-place addition of a constant to a matrix";

PyObject * 
gsl::matrix::shift(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * self;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!d:matrix_shift",
                                  &PyCapsule_Type, &self, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the two matrices
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(self, capsule_t));
    // std::cout << " gsl.matrix_shift: matrix@" << m << ", value=" << value << std::endl;
    // perform the shift
    gsl_matrix_add_constant(m, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


const char * const gsl::matrix::scale__name__ = "matrix_scale";
const char * const gsl::matrix::scale__doc__ = "in-place scaling of a matrix by a constant";

PyObject * 
gsl::matrix::scale(PyObject *, PyObject * args) {
    // the arguments
    double value;
    PyObject * self;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!d:matrix_scale",
                                  &PyCapsule_Type, &self, &value);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(self, capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the two matrices
    gsl_matrix * m = static_cast<gsl_matrix *>(PyCapsule_GetPointer(self, capsule_t));
    // std::cout << " gsl.matrix_scale: matrix@" << m << ", value=" << value << std::endl;
    // perform the scale
    gsl_matrix_scale(m, value);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// destructor
void 
gsl::matrix::free(PyObject * capsule)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, gsl::matrix::capsule_t)) return;
    // get the matrix
    gsl_matrix * m = 
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, gsl::matrix::capsule_t));
    // std::cout << " gsl.matrix_free: matrix@" << m << std::endl;
    // deallocate
    gsl_matrix_free(m);
    // and return
    return;
}


// end of file
