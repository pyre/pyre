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

#include "vector.h"

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
        { vector::allocate__name__, vector::allocate, METH_VARARGS, vector::allocate__doc__},
        { vector::zero__name__, vector::zero, METH_VARARGS, vector::zero__doc__},
        { vector::fill__name__, vector::fill, METH_VARARGS, vector::fill__doc__},
        { vector::basis__name__, vector::basis, METH_VARARGS, vector::basis__doc__},

        { vector::get__name__, vector::get, METH_VARARGS, vector::get__doc__},
        { vector::set__name__, vector::set, METH_VARARGS, vector::set__doc__},

        { vector::contains__name__, vector::contains, METH_VARARGS, vector::contains__doc__},

        { vector::add__name__, vector::add, METH_VARARGS, vector::add__doc__},
        { vector::sub__name__, vector::sub, METH_VARARGS, vector::sub__doc__},
        { vector::mul__name__, vector::mul, METH_VARARGS, vector::mul__doc__},
        { vector::div__name__, vector::div, METH_VARARGS, vector::div__doc__},
        { vector::shift__name__, vector::shift, METH_VARARGS, vector::shift__doc__},
        { vector::scale__name__, vector::scale, METH_VARARGS, vector::scale__doc__},

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
    // return the newly created module
    return module;
}

// end of file
