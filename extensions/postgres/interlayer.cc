// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

#include "interlayer.h"
#include "constants.h"


// getting connections in and out of capsules


// support for raising exceptions
// raise an OperationalError exception
PyObject *
pyre::extensions::postgres::
raiseOperationalError(string_t description)
{
    PyObject * args = PyTuple_New(0);
    PyObject * kwds = Py_BuildValue("{s:s}", "description", description);
    PyObject * exception = PyObject_Call(OperationalError, args, kwds);
    // prepare to raise the instance of OperationalError
    PyErr_SetObject(OperationalError, exception);
    // and return the error indicator
    return 0;
}


// raise a ProgrammingError exception
PyObject *
pyre::extensions::postgres::
raiseProgrammingError(string_t description, string_t command)
{
    PyObject * args = PyTuple_New(0);
    PyObject * kwds = Py_BuildValue(
                                    "{s:s, s:s}", 
                                    "description", description,
                                    "command", command
                                    );
    PyObject * exception = PyObject_Call(ProgrammingError, args, kwds);
    // prepare to raise the instance of ProgrammingError
    PyErr_SetObject(ProgrammingError, exception);
    // and return the error indicator
    return 0;
}


// end of file
