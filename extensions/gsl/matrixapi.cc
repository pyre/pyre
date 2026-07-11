// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


#include <portinfo>
#include <Python.h>
#include <gsl/gsl_matrix.h>

// the capsule names
#include "capsules.h"


// the matrix operations have all moved to pybind11; what remains here is the capsule destructor
// that {partition} still reaches for when it hands a freshly allocated matrix back to python as a
// capsule. it goes away with the last of them


// release the matrix a capsule owns
void
gsl::matrix::free(PyObject * capsule)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, gsl::matrix::capsule_t))
        return;
    // get the matrix
    gsl_matrix * m =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, gsl::matrix::capsule_t));
    // deallocate
    gsl_matrix_free(m);
    // and return
    return;
}


// end of file
