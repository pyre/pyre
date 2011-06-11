// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <iostream>

#include <Python.h>
#include <libpq-fe.h>
#include <pyre/journal.h>

#include "execute.h"
#include "constants.h"


// establish a new connection
const char * const
pyre::extensions::postgres::
execute__name__ = "execute";

const char * const
pyre::extensions::postgres::
execute__doc__ = "execute a single command";

PyObject * 
pyre::extensions::postgres::
execute(PyObject *, PyObject * args) {
    // the connection specification
    const char * command;
    PyObject * py_connection;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!s:execute", &PyCapsule_Type, &py_connection, &command)) {
        return 0;
    }
    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_connection, connectionCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid database connection");
        return 0;
    }
    // get the connection object
    PGconn * connection = 
        static_cast<PGconn *>(PyCapsule_GetPointer(py_connection, connectionCapsuleName));

    // in case someone is listening...
    pyre::journal::debug_t debug("postgres.execution");
    debug 
        << pyre::journal::at(__HERE__)
        << "executing '" << command << "'"
        << pyre::journal::endl;

    // execute the command
    PGresult * result = PQexec(connection, command);
    // error check
    if (!result) {
        PyObject * args = PyTuple_New(0);
        const char * description = PQerrorMessage(connection);
        PyObject * kwds = Py_BuildValue(
                                        "{s:s, s:s}", 
                                        "description", description,
                                        "command", command
                                        );
        PyObject * exception = PyObject_Call(OperationalError, args, kwds);
        // prepare to raise the instance of OperationalError
        PyErr_SetObject(OperationalError, exception);
        // and return the error indicator
        return 0;
    }

    // all is well
    // free the result
    PQclear(result);
    // and return
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
