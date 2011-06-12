// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>

#include <Python.h>
#include <libpq-fe.h>
#include <pyre/journal.h>

#include "interlayer.h"
#include "constants.h"


// convert the tuples in PGresult into a python tuple
PyObject *
pyre::extensions::postgres::
resultTuples(PGresult * result)
{
}


// support for raising exceptions
// raise an OperationalError exception
PyObject *
pyre::extensions::postgres::
raiseOperationalError(string_t description)
{
    PyObject * args = PyTuple_New(0);
    PyObject * kwds = Py_BuildValue("{s:s}", "description", description);
    PyObject * exception = PyObject_Call(OperationalError, args, kwds);
    // prepare to raise an instance of OperationalError
    PyErr_SetObject(OperationalError, exception);
    // and return an error indicator
    return 0;
}


// raise a ProgrammingError exception
PyObject *
pyre::extensions::postgres::
raiseProgrammingError(string_t description, string_t command)
{
    PyObject * args = PyTuple_New(0);
    PyObject * kwds = Py_BuildValue("{s:s, s:s}", 
                                    "description", description,
                                    "command", command
                                    );
    PyObject * exception = PyObject_Call(ProgrammingError, args, kwds);
    // prepare to raise an instance of ProgrammingError
    PyErr_SetObject(ProgrammingError, exception);
    // and return an error indicator
    return 0;
}


// end of file
