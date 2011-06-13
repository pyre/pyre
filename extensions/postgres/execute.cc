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


// execute a query synchronously
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
        // diagnostics
        if (debug.isActive()) {
            debug 
                << pyre::journal::at(__HERE__)
                << "success: " << PQcmdStatus(result)
                << pyre::journal::endl;
        }
        // build the return value
        Py_INCREF(Py_None);
        value = Py_None;

    } else if (PQresultStatus(result) == PGRES_TUPLES_OK) {
        // the query succeeded and there are tuples to harvest
        if (debug.isActive()) {
            int fields = PQnfields(result);
            int tuples = PQntuples(result);
            debug 
                << pyre::journal::at(__HERE__)
                << "success: " 
                << tuples << " tuple" << (tuples == 1 ? "" : "s")
                << " with " << fields << " field" << (fields == 1 ? "" : "s") << " each"
                << pyre::journal::endl;
        }
        // build the return value
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


// submit a query for asynchronous execution
const char * const
pyre::extensions::postgres::
submit__name__ = "submit";

const char * const
pyre::extensions::postgres::
submit__doc__ = "submit a command for asynchronous execution";

PyObject * 
pyre::extensions::postgres::
submit(PyObject *, PyObject * args) {
    // the connection specification
    const char * command;
    PyObject * py_connection;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!s:submit", &PyCapsule_Type, &py_connection, &command)) {
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
        << "submitting '" << command << "'"
        << pyre::journal::endl;

    // submit the query
    int status = PQsendQuery(connection, command);

    // error check
    // null status indicates a problem with submitting the request
    if (!status) {
        // convert the error to human readable form
        const char * description = PQerrorMessage(connection);
        // and return an error indicator
        return raiseOperationalError(description);
    }

    // return None
    Py_INCREF(Py_None);
    return Py_None;
}


// check whether a query result set has been computed
const char * const
pyre::extensions::postgres::
consume__name__ = "consume";

const char * const
pyre::extensions::postgres::
consume__doc__ = "submit a command for asynchronous execution";

PyObject * 
pyre::extensions::postgres::
consume(PyObject *, PyObject * args) {
    // the connection specification
    PyObject * py_connection;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:consume", &PyCapsule_Type, &py_connection)) {
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

    // consume the available partial result
    PQconsumeInput(connection);

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// retrieve a query result
const char * const
pyre::extensions::postgres::
retrieve__name__ = "retrieve";

const char * const
pyre::extensions::postgres::
retrieve__doc__ = "retrieve a result set from a previously submitted asynchronous query";

PyObject * 
pyre::extensions::postgres::
retrieve(PyObject *, PyObject * args) {
    // the connection specification
    PyObject * py_connection;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:retrieve", &PyCapsule_Type, &py_connection)) {
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

    // MGA: NYI
    pyre::journal::error_t error("postgres.NYI");
    error
        << pyre::journal::at(__HERE__)
        << "postgres.retrieve: NYI" 
        << pyre::journal::endl;
    // retrieve the result
    PQgetResult(connection);

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// check whether a query result set has been computed
const char * const
pyre::extensions::postgres::
resultAvailable__name__ = "resultAvailable";

const char * const
pyre::extensions::postgres::
resultAvailable__doc__ = "check the availability of a result set from a previously submitted query";

PyObject * 
pyre::extensions::postgres::
resultAvailable(PyObject *, PyObject * args) {
    // the connection specification
    PyObject * py_connection;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:resultAvailable", &PyCapsule_Type, &py_connection)) {
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

    // check
    if (PQisBusy(connection) == 0) {
        Py_INCREF(Py_True);
        return Py_True;
    }

    // otherwise
    Py_INCREF(Py_False);
    return Py_False;
}


// end of file
