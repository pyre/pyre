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

#include "execute.h"
#include "constants.h"
#include "interlayer.h"


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
    // null result indicates we have run out of memory
    if (!result) {
        // convert the error to human readable form
        const char * description = PQerrorMessage(connection);
        // and return an error indicator
        return raiseOperationalError(description);
    }

    //  this is what we will return to the caller
    PyObject * value;
    if (PQresultStatus(result) == PGRES_COMMAND_OK) {
        // the command was executed successfully
        debug 
            << pyre::journal::at(__HERE__)
            << "success: command: '" << command << "'"
            << pyre::journal::endl;
        // None for now
        Py_INCREF(Py_None);
        value = Py_None;

    } else if (PQresultStatus(result) == PGRES_TUPLES_OK) {
        // the query succeeded and there are tuples to harvest
        debug 
            << pyre::journal::at(__HERE__)
            << "success: query: '" << command << "'"
            << pyre::journal::endl;
        value = stringTuple(result);
    } else {
        // there was something wrong with the command
        const char * description = PQresultErrorMessage(result);
        // raise a ProgrammingError
        value = raiseProgrammingError(description, command);
    }

    // all is well
    // free the result
    PQclear(result);
    // and return
    return value;
}

// end of file
