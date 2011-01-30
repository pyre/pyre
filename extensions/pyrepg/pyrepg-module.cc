// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// the module method declarations
#include "pyrepg-metadata.h"

// put everything in my private namespace
namespace pyrepg {

    // the module method table
    PyMethodDef methods[] = {
        // the copyright method
        { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
        // the version method
        { version__name__, version, METH_VARARGS, version__doc__ },

        // sentinel
        {0, 0, 0, 0}
    };


    // the module documentation string
    const char * const doc = "provides access to PostgreSQL databases";

    // the module definition structure
    PyModuleDef module = {
        // header
        PyModuleDef_HEAD_INIT,
        // the name of the module
        "pyrepg",
        // the module documentation string
        doc,
        // size of the per-interpreter state of the module; -1 if this state is global
        -1,
        // the methods defined in this module
        methods
    };

} // of namespace pyrepg


// initialization function for the module
// *must* be called PyInit_pyrepg
PyMODINIT_FUNC
PyInit_pyrepg()
{
    return PyModule_Create(&pyrepg::module);
}


// end of file
