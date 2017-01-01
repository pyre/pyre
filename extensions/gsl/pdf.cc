// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//


#include <portinfo>
#include <Python.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_randist.h>

// local includes
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


// uniform::vector
const char * const gsl::pdf::uniform::vector__name__ = "uniform_vector";
const char * const gsl::pdf::uniform::vector__doc__ = "fill a vector with random values";

PyObject *
gsl::pdf::uniform::vector(PyObject *, PyObject * args) {
    // the arguments
    double a, b;
    PyObject * rngCapsule;
    PyObject * vectorCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "(dd)O!O!:uniform_vector",
                                  &a, &b,
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &vectorCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the vector capsule is not valid
    if (!PyCapsule_IsValid(vectorCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the vector
    gsl_vector * v =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(vectorCapsule, gsl::vector::capsule_t));
    // fill
    for (size_t i = 0; i < v->size; i++) {
        double value = gsl_ran_flat(rng, a, b);
        gsl_vector_set(v, i, value);
    }
    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// uniform::matrix
const char * const gsl::pdf::uniform::matrix__name__ = "uniform_matrix";
const char * const gsl::pdf::uniform::matrix__doc__ = "fill a matrix with random values";

PyObject *
gsl::pdf::uniform::matrix(PyObject *, PyObject * args) {
    // the arguments
    double a, b;
    PyObject * rngCapsule;
    PyObject * matrixCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "(dd)O!O!:uniform_matrix",
                                  &a, &b,
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &matrixCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the matrix capsule is not valid
    if (!PyCapsule_IsValid(matrixCapsule, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the matrix
    gsl_matrix * m =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(matrixCapsule, gsl::matrix::capsule_t));
    // fill
    for (size_t i = 0; i < m->size1; i++) {
        for (size_t j = 0; j < m->size2; j++) {
            double value = gsl_ran_flat(rng, a, b);
            gsl_matrix_set(m, i, j, value);
        }
    }
    // return None
    Py_INCREF(Py_None);
    return Py_None;
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
    // sample the distribution
    double sample = gsl_ran_gaussian(r, sigma);

    // return the value
    return PyFloat_FromDouble(sample);
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

    // compute
    double pdf = gsl_ran_gaussian_pdf(x, sigma);

    // compute the density and return the value
    return PyFloat_FromDouble(pdf);
}


// gaussian::vector
const char * const gsl::pdf::gaussian::vector__name__ = "gaussian_vector";
const char * const gsl::pdf::gaussian::vector__doc__ = "fill a vector with random values";

PyObject *
gsl::pdf::gaussian::vector(PyObject *, PyObject * args) {
    // the arguments
    double sigma;
    PyObject * rngCapsule;
    PyObject * vectorCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "dO!O!:gaussian_vector",
                                  &sigma,
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &vectorCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the vector capsule is not valid
    if (!PyCapsule_IsValid(vectorCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the vector
    gsl_vector * v =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(vectorCapsule, gsl::vector::capsule_t));
    // fill
    for (size_t i = 0; i < v->size; i++) {
        double value = gsl_ran_gaussian(rng, sigma);
        gsl_vector_set(v, i, value);
    }
    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// gaussian::matrix
const char * const gsl::pdf::gaussian::matrix__name__ = "gaussian_matrix";
const char * const gsl::pdf::gaussian::matrix__doc__ = "fill a matrix with random values";

PyObject *
gsl::pdf::gaussian::matrix(PyObject *, PyObject * args) {
    // the arguments
    double sigma;
    PyObject * rngCapsule;
    PyObject * matrixCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "dO!O!:gaussian_matrix",
                                  &sigma,
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &matrixCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the matrix capsule is not valid
    if (!PyCapsule_IsValid(matrixCapsule, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the matrix
    gsl_matrix * m =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(matrixCapsule, gsl::matrix::capsule_t));
    // fill
    for (size_t i = 0; i < m->size1; i++) {
        for (size_t j = 0; j < m->size2; j++) {
            double value = gsl_ran_gaussian(rng, sigma);
            gsl_matrix_set(m, i, j, value);
        }
    }
    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// ugaussian::sample
const char * const gsl::pdf::ugaussian::sample__name__ = "ugaussian_sample";
const char * const gsl::pdf::ugaussian::sample__doc__ =
    "return a sample from the unit gaussian distribution";

PyObject *
gsl::pdf::ugaussian::sample(PyObject *, PyObject * args) {
    // the arguments
    PyObject * capsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!:ugaussian_sample",
                                  &PyCapsule_Type, &capsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }

    // get the rng
    gsl_rng * r = static_cast<gsl_rng *>(PyCapsule_GetPointer(capsule, gsl::rng::capsule_t));
    // sample the distribution
    double sample = gsl_ran_ugaussian(r);

    // and return the value
    return PyFloat_FromDouble(sample);
}


// ugaussian::density
const char * const gsl::pdf::ugaussian::density__name__ = "ugaussian_density";
const char * const gsl::pdf::ugaussian::density__doc__ =
    "return the unit gaussian distribution density";

PyObject *
gsl::pdf::ugaussian::density(PyObject *, PyObject * args) {
    // the arguments
    double x;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(args, "d:ugaussian_density", &x);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;

    // compute the density and return the value
    double pdf = gsl_ran_ugaussian_pdf(x);

    // and return the value
    return PyFloat_FromDouble(pdf);
}


// ugaussian::vector
const char * const gsl::pdf::ugaussian::vector__name__ = "ugaussian_vector";
const char * const gsl::pdf::ugaussian::vector__doc__ = "fill a vector with random values";

PyObject *
gsl::pdf::ugaussian::vector(PyObject *, PyObject * args) {
    // the arguments
    PyObject * rngCapsule;
    PyObject * vectorCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:ugaussian_vector",
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &vectorCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the vector capsule is not valid
    if (!PyCapsule_IsValid(vectorCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the vector
    gsl_vector * v =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(vectorCapsule, gsl::vector::capsule_t));
    // fill
    for (size_t i = 0; i < v->size; i++) {
        double value = gsl_ran_ugaussian(rng);
        gsl_vector_set(v, i, value);
    }
    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// ugaussian::matrix
const char * const gsl::pdf::ugaussian::matrix__name__ = "ugaussian_matrix";
const char * const gsl::pdf::ugaussian::matrix__doc__ = "fill a matrix with random values";

PyObject *
gsl::pdf::ugaussian::matrix(PyObject *, PyObject * args) {
    // the arguments
    PyObject * rngCapsule;
    PyObject * matrixCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!:ugaussian_matrix",
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &matrixCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the matrix capsule is not valid
    if (!PyCapsule_IsValid(matrixCapsule, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the matrix
    gsl_matrix * m =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(matrixCapsule, gsl::matrix::capsule_t));
    // fill
    for (size_t i = 0; i < m->size1; i++) {
        for (size_t j = 0; j < m->size2; j++) {
            double value = gsl_ran_ugaussian(rng);
            gsl_matrix_set(m, i, j, value);
        }
    }
    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// dirichlet::vector
const char * const gsl::pdf::dirichlet::vector__name__ = "dirichlet_vector";
const char * const gsl::pdf::dirichlet::vector__doc__ = "fill a vector with random values";

PyObject *
gsl::pdf::dirichlet::vector(PyObject *, PyObject * args) {
    // the arguments
    PyObject * rngCapsule;
    PyObject * alphaCapsule;
    PyObject * vectorCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!O!:dirichlet_vector",
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &alphaCapsule,
                                  &PyCapsule_Type, &vectorCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the alpha capsule is not valid
    if (!PyCapsule_IsValid(alphaCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }
    // bail out if the vector capsule is not valid
    if (!PyCapsule_IsValid(vectorCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }

    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the vector
    gsl_vector * alpha =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(alphaCapsule, gsl::vector::capsule_t));
    // get the vector
    gsl_vector * v =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(vectorCapsule, gsl::vector::capsule_t));

    // get the order of the pdf
    size_t K = alpha->size;
    // check that it is compatible with the matrix we were given
    if (K != v->size) {
        PyErr_SetString(PyExc_ValueError, "shape incompatibility");
        return 0;
    }
    // fill the vector
    gsl_ran_dirichlet(rng, K, alpha->data, v->data);

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// dirichlet::matrix
const char * const gsl::pdf::dirichlet::matrix__name__ = "dirichlet_matrix";
const char * const gsl::pdf::dirichlet::matrix__doc__ = "fill a matrix with random values";

PyObject *
gsl::pdf::dirichlet::matrix(PyObject *, PyObject * args) {
    // the arguments
    PyObject * rngCapsule;
    PyObject * alphaCapsule;
    PyObject * matrixCapsule;
    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!O!:dirichlet_matrix",
                                  &PyCapsule_Type, &rngCapsule,
                                  &PyCapsule_Type, &alphaCapsule,
                                  &PyCapsule_Type, &matrixCapsule);
    // bail out if something went wrong with the argument unpacking
    if (!status) return 0;
    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }
    // bail out if the alpha capsule is not valid
    if (!PyCapsule_IsValid(alphaCapsule, gsl::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule");
        return 0;
    }
    // bail out if the matrix capsule is not valid
    if (!PyCapsule_IsValid(matrixCapsule, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }
    // get the rng
    gsl_rng * rng =
        static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    // get the vector
    gsl_vector * alpha =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(alphaCapsule, gsl::vector::capsule_t));
    // get the matrix
    gsl_matrix * m =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(matrixCapsule, gsl::matrix::capsule_t));

    // get the order of the pdf
    size_t K = alpha->size;
    // check that it is compatible with the matrix we were given
    if (K != m->size2) {
        PyErr_SetString(PyExc_ValueError, "shape incompatibility");
        return 0;
    }

    // fill
    for (size_t i = 0; i < m->size1; i++) {
        // fill the row
        gsl_ran_dirichlet(rng, K, alpha->data, m->data + i*m->size2);
    }

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// end of file
