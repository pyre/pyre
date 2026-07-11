// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


#include <portinfo>
#include <Python.h>
#include <gsl/gsl_vector.h>

// the capsule names
#include "capsules.h"


// the vector operations have all moved to pybind11; what remains here is the capsule destructor
// that {matrixapi} and {partition} still reach for when they hand a freshly allocated vector back
// to python as a capsule. it goes away with the last of them


// release the vector a capsule owns
void
gsl::vector::free(PyObject * capsule)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, gsl::vector::capsule_t))
        return;
    // get the vector
    gsl_vector * v =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, gsl::vector::capsule_t));
    // deallocate
    gsl_vector_free(v);
    // and return
    return;
}


// end of file
