// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

// for the build system
#include <portinfo>
// external dependencies
#include <string>
#include <Python.h>

// the module method declarations
#include "exceptions.h"
#include "metadata.h"

#include "matrix.h" // matrices
#include "vector.h" // vectors
#include "rng.h" // random numbers
#include "pdf.h" // probability distribution functions

// put everything in my private namespace
namespace gsl {
        
    // the module method table
    PyMethodDef module_methods[] = {
        // module metadata
        // the copyright method
        { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
        // the license
        { license__name__, license, METH_VARARGS, license__doc__ },
        // the version
        { version__name__, version, METH_VARARGS, version__doc__ },

        // vectors
        { vector::alloc__name__, vector::alloc, METH_VARARGS, vector::alloc__doc__ },
        { vector::zero__name__, vector::zero, METH_VARARGS, vector::zero__doc__ },
        { vector::fill__name__, vector::fill, METH_VARARGS, vector::fill__doc__ },
        { vector::basis__name__, vector::basis, METH_VARARGS, vector::basis__doc__ },
        { vector::copy__name__, vector::copy, METH_VARARGS, vector::copy__doc__ },
        { vector::get__name__, vector::get, METH_VARARGS, vector::get__doc__ },
        { vector::set__name__, vector::set, METH_VARARGS, vector::set__doc__ },
        { vector::contains__name__, vector::contains, METH_VARARGS, vector::contains__doc__ },
        { vector::max__name__, vector::max, METH_VARARGS, vector::max__doc__ },
        { vector::min__name__, vector::min, METH_VARARGS, vector::min__doc__ },
        { vector::minmax__name__, vector::minmax, METH_VARARGS, vector::minmax__doc__ },
        { vector::add__name__, vector::add, METH_VARARGS, vector::add__doc__ },
        { vector::sub__name__, vector::sub, METH_VARARGS, vector::sub__doc__ },
        { vector::mul__name__, vector::mul, METH_VARARGS, vector::mul__doc__ },
        { vector::div__name__, vector::div, METH_VARARGS, vector::div__doc__ },
        { vector::shift__name__, vector::shift, METH_VARARGS, vector::shift__doc__ },
        { vector::scale__name__, vector::scale, METH_VARARGS, vector::scale__doc__ },

        // matrices
        { matrix::alloc__name__, matrix::alloc, METH_VARARGS, matrix::alloc__doc__ },
        { matrix::zero__name__, matrix::zero, METH_VARARGS, matrix::zero__doc__ },
        { matrix::fill__name__, matrix::fill, METH_VARARGS, matrix::fill__doc__ },
        { matrix::identity__name__, matrix::identity, METH_VARARGS, matrix::identity__doc__ },
        { matrix::copy__name__, matrix::copy, METH_VARARGS, matrix::copy__doc__ },
        { matrix::get__name__, matrix::get, METH_VARARGS, matrix::get__doc__ },
        { matrix::set__name__, matrix::set, METH_VARARGS, matrix::set__doc__ },
        { matrix::contains__name__, matrix::contains, METH_VARARGS, matrix::contains__doc__ },
        { matrix::max__name__, matrix::max, METH_VARARGS, matrix::max__doc__ },
        { matrix::min__name__, matrix::min, METH_VARARGS, matrix::min__doc__ },
        { matrix::minmax__name__, matrix::minmax, METH_VARARGS, matrix::minmax__doc__ },
        { matrix::add__name__, matrix::add, METH_VARARGS, matrix::add__doc__ },
        { matrix::sub__name__, matrix::sub, METH_VARARGS, matrix::sub__doc__ },
        { matrix::mul__name__, matrix::mul, METH_VARARGS, matrix::mul__doc__ },
        { matrix::div__name__, matrix::div, METH_VARARGS, matrix::div__doc__ },
        { matrix::shift__name__, matrix::shift, METH_VARARGS, matrix::shift__doc__ },
        { matrix::scale__name__, matrix::scale, METH_VARARGS, matrix::scale__doc__ },

        // random numbers
        { rng::avail__name__, rng::avail, METH_VARARGS, rng::avail__doc__ },
        { rng::alloc__name__, rng::alloc, METH_VARARGS, rng::alloc__doc__ },
        { rng::set__name__, rng::set, METH_VARARGS, rng::set__doc__ },
        { rng::name__name__, rng::name, METH_VARARGS, rng::name__doc__ },
        { rng::range__name__, rng::range, METH_VARARGS, rng::range__doc__ },

        { rng::get__name__, rng::get, METH_VARARGS, rng::get__doc__ },
        { rng::uniform__name__, rng::uniform, METH_VARARGS, rng::uniform__doc__ },

        // probability distribution functions
        { pdf::uniform::sample__name__, pdf::uniform::sample, METH_VARARGS,
          pdf::uniform::sample__doc__ },
        { pdf::uniform::density__name__, pdf::uniform::density, METH_VARARGS,
          pdf::uniform::density__doc__ },
        { pdf::uniform::vector__name__, pdf::uniform::vector, METH_VARARGS,
          pdf::uniform::vector__doc__ },
        { pdf::uniform::matrix__name__, pdf::uniform::matrix, METH_VARARGS,
          pdf::uniform::matrix__doc__ },

        { pdf::gaussian::sample__name__, pdf::gaussian::sample, METH_VARARGS,
          pdf::gaussian::sample__doc__ },
        { pdf::gaussian::density__name__, pdf::gaussian::density, METH_VARARGS,
          pdf::gaussian::density__doc__ },
        { pdf::gaussian::vector__name__, pdf::gaussian::vector, METH_VARARGS,
          pdf::gaussian::vector__doc__ },
        { pdf::gaussian::matrix__name__, pdf::gaussian::matrix, METH_VARARGS,
          pdf::gaussian::matrix__doc__ },

        // sentinel
        {0, 0, 0, 0}
    };

    // the module documentation string
    const char * const __doc__ = "sample module documentation string";

    // the module definition structure
    PyModuleDef module_definition = {
        // header
        PyModuleDef_HEAD_INIT,
        // the name of the module
        "gsl", 
        // the module documentation string
        __doc__,
        // size of the per-interpreter state of the module; -1 if this state is global
        -1,
        // the methods defined in this module
        module_methods
    };
} // of namespace gsl


// initialization function for the module
// *must* be called PyInit_gsl
PyMODINIT_FUNC
PyInit_gsl()
{
    // create the module
    PyObject * module = PyModule_Create(&gsl::module_definition);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return 0;
    }
    // otherwise, we have an initialized module
    // initialize the table of known random number generators
    gsl::rng::initialize();

    // return the newly created module
    return module;
}

// end of file
