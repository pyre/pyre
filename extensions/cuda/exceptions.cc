// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2024 all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <string>

// my declarations
#include "exceptions.h"

// allocate the global objects
namespace pyre::extensions::cuda {
    PyObject * Error = nullptr;
} // namespace pyre::extensions::cuda


// exception registration
const char * const pyre::extensions::cuda::registerExceptions__name__ = "registerExceptions";

const char * const pyre::extensions::cuda::registerExceptions__doc__ =
    "register the classes that represent the standard exceptions raised by CUDA";

PyObject *
pyre::extensions::cuda::registerExceptions(PyObject * module, PyObject * args)
{
    // unpack the arguments
    PyObject * exceptions;
    if (!PyArg_ParseTuple(args, "O!:registerExceptions", &PyModule_Type, &exceptions)) {
        return nullptr;
    }

    // register the base class
    Error = PyObject_GetAttrString(exceptions, "Error");
    PyModule_AddObject(module, "Error", Error);

    // and return the module
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
