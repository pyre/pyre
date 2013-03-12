// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2013 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// the module method declarations
#include "metadata.h"

// put everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace cuda {

            // the module method table
            PyMethodDef methods[] = {
                // module metadata
                // copyright
                { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
                // version
                { version__name__, version, METH_VARARGS, version__doc__ },
                // license
                { license__name__, license, METH_VARARGS, license__doc__ },

                // sentinel
                {0, 0, 0, 0}
            };


            // the module documentation string
            const char * const doc = "provides access to CUDA enabled devices";

            // the module definition structure
            PyModuleDef module = {
                // header
                PyModuleDef_HEAD_INIT,
                // the name of the module
                "cuda",
                // the module documentation string
                doc,
                // size of the per-interpreter state of the module; -1 if this state is global
                -1,
                // the methods defined in this module
                methods
            };

        } // of namespace cuda
    } // of namespace extensions
} // of namespace pyre

// initialization function for the module
// *must* be called PyInit_cuda
PyMODINIT_FUNC
PyInit_cuda()
{
    // create the module
    PyObject * module = PyModule_Create(&pyre::extensions::cuda::module);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return module;
    }
    // module initialization
    // return the newly created module
    return module;
}


// end of file
