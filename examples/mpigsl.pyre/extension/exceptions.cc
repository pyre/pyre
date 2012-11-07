// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <string>

#include "exceptions.h"

namespace mpigsl {
    // base class for mpigsl errors
    const char * const Error__name__ = "Error";
    PyObject * Error = 0;
    
} // of namespace mpigsl


// exception registration
PyObject * 
mpigsl::
registerExceptionHierarchy(PyObject * module) {

    std::string stem = "mpigsl.";

    // the base class
    // build its name
    std::string errorName = stem + mpigsl::Error__name__;
    // and the exception object
    mpigsl::Error = PyErr_NewException(errorName.c_str(), 0, 0);
    // increment its reference count so we can pass ownership to the module
    Py_INCREF(mpigsl::Error);
    // register it with the module
    PyModule_AddObject(module, mpigsl::Error__name__, mpigsl::Error);

    // and return the module
    return module;
}

// end of file
