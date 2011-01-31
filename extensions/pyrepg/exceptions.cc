// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <string>

#include "exceptions.h"

namespace pyrepg {
    // base class for pyrepg errors
    const char * const Error__name__ = "Error";
    PyObject * Error = 0;
}


// exception registration
PyObject * pyrepg::registerExceptionHierarchy(PyObject * module) {
    // prefix for the exception names so that python can decorate the classes properly
    std::string stem = "pyrepg.";

    // the base class
    // build its name
    std::string errorName = stem + pyrepg::Error__name__;
    // and the exception object
    pyrepg::Error = PyErr_NewException(errorName.c_str(), PyExc_Exception, 0);
    // increment its reference count so we can pass ownership to the module
    Py_INCREF(pyrepg::Error);
    // register it with the module
    PyModule_AddObject(module, pyrepg::Error__name__, pyrepg::Error);

    // and return the module
    return module;
}

// end of file
