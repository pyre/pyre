// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <string>
#include <iostream>

#include "exceptions.h"

namespace pyrepg {
    // exception hierarchy for pyrepg errors
    PyObject * Error = 0;
    PyObject * Warning = 0;
    PyObject * InterfaceError = 0;
    PyObject * DatabaseError = 0;
    PyObject * DataError = 0;
    PyObject * OperationalError = 0;
    PyObject * IntegrityError = 0;
    PyObject * InternalError = 0;
    PyObject * ProgrammingError = 0;
    PyObject * NotSupportedError = 0;
}


// exception registration
PyObject * pyrepg::registerExceptions(PyObject * module, PyObject * args) {

    // unpack the arguments
    PyObject * exceptions;
    if (!PyArg_ParseTuple(args, "O!:registerExceptions", &PyModule_Type, &exceptions)) {
        return 0;
    }

    // keep a record of the standard exception classes and register them with the module
    pyrepg::Warning = PyObject_GetAttrString(exceptions, "Warning");
    PyModule_AddObject(module, "Warning", pyrepg::Warning);

    pyrepg::Error = PyObject_GetAttrString(exceptions, "Error");
    PyModule_AddObject(module, "Error", pyrepg::Error);

    pyrepg::InterfaceError = PyObject_GetAttrString(exceptions, "InterfaceError");
    PyModule_AddObject(module, "InterfaceError", pyrepg::InterfaceError);

    pyrepg::DatabaseError = PyObject_GetAttrString(exceptions, "DatabaseError");
    PyModule_AddObject(module, "DatabaseError", pyrepg::DatabaseError);

    pyrepg::DataError = PyObject_GetAttrString(exceptions, "DataError");
    PyModule_AddObject(module, "DataError", pyrepg::DataError);

    pyrepg::OperationalError = PyObject_GetAttrString(exceptions, "OperationalError");
    PyModule_AddObject(module, "OperationalError", pyrepg::OperationalError);

    pyrepg::IntegrityError = PyObject_GetAttrString(exceptions, "IntegrityError");
    PyModule_AddObject(module, "IntegrityError", pyrepg::IntegrityError);

    pyrepg::InternalError = PyObject_GetAttrString(exceptions, "InternalError");
    PyModule_AddObject(module, "InternalError", pyrepg::InternalError);

    pyrepg::ProgrammingError = PyObject_GetAttrString(exceptions, "ProgrammingError");
    PyModule_AddObject(module, "ProgrammingError", pyrepg::ProgrammingError);

    pyrepg::NotSupportedError = PyObject_GetAttrString(exceptions, "NotSupportedError");
    PyModule_AddObject(module, "NotSupportedError", pyrepg::NotSupportedError);

    // and return the module
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
