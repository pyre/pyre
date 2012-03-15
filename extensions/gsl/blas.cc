// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 


#include <portinfo>
#include <Python.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>

// local includes
#include "blas.h"
#include "capsules.h"


// blas::ddot
const char * const gsl::blas::ddot__name__ = "blas_ddot";
const char * const gsl::blas::ddot__doc__ = "compute the scalar product of two vectors";

PyObject * 
gsl::blas::ddot(PyObject *, PyObject * args) {
    // the arguments
    PyObject * v1c;
    PyObject * v2c;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:blas_ddot",
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
    gsl_blas_ddot(v1, v2, &result);
    // and return the result
    return PyFloat_FromDouble(result);
}


// blas::dnrm2
const char * const gsl::blas::dnrm2__name__ = "blas_dnrm2";
const char * const gsl::blas::dnrm2__doc__ = "compute the Euclidean norm of a vector";

PyObject * 
gsl::blas::dnrm2(PyObject *, PyObject * args) {
    // the arguments
    PyObject * vc;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:blas_dnrm2", &PyCapsule_Type, &vc);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(vc, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(vc, gsl::vector::capsule_t));
    // compute the norm
    double norm = gsl_blas_dnrm2(v);
    // and return the result
    return PyFloat_FromDouble(norm);
}


// blas::dasum
const char * const gsl::blas::dasum__name__ = "blas_dasum";
const char * const gsl::blas::dasum__doc__ = 
    "compute the sum of the absolute values of the vector entries";

PyObject * 
gsl::blas::dasum(PyObject *, PyObject * args) {
    // the arguments
    PyObject * vc;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "O!:blas_dasum", &PyCapsule_Type, &vc);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(vc, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the vector
    gsl_vector * v = static_cast<gsl_vector *>(PyCapsule_GetPointer(vc, gsl::vector::capsule_t));
    // compute the norm
    double norm = gsl_blas_dasum(v);
    // and return the result
    return PyFloat_FromDouble(norm);
}


// blas::daxpy
const char * const gsl::blas::daxpy__name__ = "blas_daxpy";
const char * const gsl::blas::daxpy__doc__ = "compute the scalar product of two vectors";

PyObject * 
gsl::blas::daxpy(PyObject *, PyObject * args) {
    // the arguments
    double a;
    PyObject * v1c;
    PyObject * v2c;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "dO!O!:blas_daxpy",
                                  &a, &PyCapsule_Type, &v1c, &PyCapsule_Type, &v2c);
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
    // compute the form
    gsl_blas_daxpy(a, v1, v2);
    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// blas::dtrmv
const char * const gsl::blas::dtrmv__name__ = "blas_dtrmv";
const char * const gsl::blas::dtrmv__doc__ = "compute y = a A x + b y";

PyObject * 
gsl::blas::dtrmv(PyObject *, PyObject * args) {
    // the arguments
    int uplo, op, unitDiag;
    PyObject * xc;
    PyObject * Ac;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "iiiO!O!:blas_dtrmv",
                                  &uplo, &op, &unitDiag,
                                  &PyCapsule_Type, &Ac,
                                  &PyCapsule_Type, &xc);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(Ac, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the third argument must be a matrix");
        return 0;
    }
    if (!PyCapsule_IsValid(xc, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the fourth argument must be a vector");
        return 0;
    }

    // decode the enums
    CBLAS_UPLO_t cuplo = uplo ? CblasUpper : CblasLower;
    CBLAS_DIAG_t cdiag = unitDiag ? CblasUnit : CblasNonUnit;
    CBLAS_TRANSPOSE_t ctran;
    switch(op) {
    case 0:
        ctran = CblasNoTrans; break;
    case 1:
        ctran = CblasTrans; break;
    case 2:
        ctran = CblasConjTrans; break;
    default:
        PyErr_SetString(PyExc_TypeError, "bad operation flag");
        return 0;
    }

    // get the two vectors
    gsl_vector * x = static_cast<gsl_vector *>(PyCapsule_GetPointer(xc, gsl::vector::capsule_t));
    // get the matrix
    gsl_matrix * A = static_cast<gsl_matrix *>(PyCapsule_GetPointer(Ac, gsl::matrix::capsule_t));
    // compute the form
    gsl_blas_dtrmv(cuplo, ctran, cdiag, A, x);
    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// blas::dsymv
const char * const gsl::blas::dsymv__name__ = "blas_dsymv";
const char * const gsl::blas::dsymv__doc__ = "compute y = a A x + b y";

PyObject * 
gsl::blas::dsymv(PyObject *, PyObject * args) {
    // the arguments
    int uplo;
    double a, b;
    PyObject * xc;
    PyObject * yc;
    PyObject * Ac;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "idO!O!dO!:blas_dsymv",
                                  &uplo,
                                  &a,
                                  &PyCapsule_Type, &Ac,
                                  &PyCapsule_Type, &xc,
                                  &b,
                                  &PyCapsule_Type, &yc);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(Ac, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the third argument must be a matrix");
        return 0;
    }
    if (!PyCapsule_IsValid(xc, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the fourth argument must be a vector");
        return 0;
    }
    if (!PyCapsule_IsValid(yc, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the sixth argument must be a vector");
        return 0;
    }

    // decode the enum
    CBLAS_UPLO_t cuplo = uplo ? CblasUpper : CblasLower;
    // get the two vectors
    gsl_vector * x = static_cast<gsl_vector *>(PyCapsule_GetPointer(xc, gsl::vector::capsule_t));
    gsl_vector * y = static_cast<gsl_vector *>(PyCapsule_GetPointer(yc, gsl::vector::capsule_t));
    // get the matrix
    gsl_matrix * A = static_cast<gsl_matrix *>(PyCapsule_GetPointer(Ac, gsl::matrix::capsule_t));
    // compute the form
    gsl_blas_dsymv(cuplo, a, A, x, b, y);
    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// blas::dsyr
const char * const gsl::blas::dsyr__name__ = "blas_dsyr";
const char * const gsl::blas::dsyr__doc__ = "compute A = a x x^T + A";

PyObject * 
gsl::blas::dsyr(PyObject *, PyObject * args) {
    // the arguments
    int uplo;
    double a;
    PyObject * xc;
    PyObject * Ac;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "idO!O!:blas_dsyr",
                                  &uplo,
                                  &a,
                                  &PyCapsule_Type, &xc,
                                  &PyCapsule_Type, &Ac);
    // if something went wrong
    if (!status) return 0;
    // bail out if the two capsules are not valid
    if (!PyCapsule_IsValid(Ac, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the fourth argument must be a matrix");
        return 0;
    }
    if (!PyCapsule_IsValid(xc, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the third argument must be a vector");
        return 0;
    }

    // decode the enum
    CBLAS_UPLO_t cuplo = uplo ? CblasUpper : CblasLower;
    // get the two vectors
    gsl_vector * x = static_cast<gsl_vector *>(PyCapsule_GetPointer(xc, gsl::vector::capsule_t));
    // get the matrix
    gsl_matrix * A = static_cast<gsl_matrix *>(PyCapsule_GetPointer(Ac, gsl::matrix::capsule_t));
    // compute the form
    gsl_blas_dsyr(cuplo, a, x, A);
    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// end of file
