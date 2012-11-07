// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// the module method declarations
#include "exceptions.h"
#include "metadata.h"
#include "partition.h"


// put everything in my private namespace
namespace mpigsl {
    // the module method table
    PyMethodDef module_methods[] = {
        // the copyright method
        { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
        // the version
        { version__name__, version, METH_VARARGS, version__doc__ },

        // matrix partitioning
        { gather__name__, gather, METH_VARARGS, gather__doc__ },
        { scatter__name__, scatter, METH_VARARGS, scatter__doc__ },
        
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
        "mpigsl", 
        // the module documentation string
        __doc__,
        // size of the per-interpreter state of the module; -1 if this state is global
        -1,
        // the methods defined in this module
        module_methods
    };

} // of namespace mpigsl


// initialization function for the module
// *must* be called PyInit_mpigsl
PyMODINIT_FUNC
PyInit_mpigsl()
{
    // create the module
    PyObject * module = PyModule_Create(&mpigsl::module_definition);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return module;
    }
    // otherwise, we have an initialized module
    mpigsl::registerExceptionHierarchy(module);

    // and return the newly created module
    return module;
}

// end of file
