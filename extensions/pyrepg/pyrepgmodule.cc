// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// the module method declarations
#include "misc.h"

// the module method table
static PyMethodDef pyrepg__methods__[] = {
    // the copyright method
    { pypyrepg_copyright__name__,
      pypyrepg_copyright, METH_VARARGS,
      pypyrepg_copyright__doc__
    },

    // the version method
    { pypyrepg_version__name__,
      pypyrepg_version, METH_VARARGS,
      pypyrepg_version__doc__
    },

    // sentinel
    {0, 0, 0, 0}
};

// the module documentation string
const char * const pyrepg__doc__ = "the module documentation string";

// the module definition structure
static struct PyModuleDef pyrepg__module__ = {
    PyModuleDef_HEAD_INIT,
    "pyrepg", // the name of the module
    pyrepg__doc__, // the module documentation string
    -1, // size of the per-interpreter state of the module; -1 if this state is global
    pyrepg__methods__
};

// initialization function for the module
// *must* be called PyInit_pyrepg
PyMODINIT_FUNC
PyInit_pyrepg()
{
    return PyModule_Create(&pyrepg__module__);
}

// end of file
