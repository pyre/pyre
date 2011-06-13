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
stringTuple(PGresult * result)
{
    // find out how many tuples in the result
    int tuples = PQntuples(result);
    // and how many fields in each tuple
    int fields = PQnfields(result);
    // build a python tuple to hold the data
    PyObject * data = PyTuple_New(tuples+1);

    // build a tuple to hold the names of the fields
    PyObject * header = PyTuple_New(fields); 
    // populate the header tuple with the names of the fields
    for (int field = 0; field < fields; field++) {
        // add the field name to the tuple
        PyTuple_SET_ITEM(header, field, PyUnicode_FromString(PQfname(result, field)));
    }
    // add the header to the data set
    PyTuple_SET_ITEM(data, 0, header);

    // iterate over the rows
    for (int tuple = 0; tuple < tuples; tuple++) {
        // build a tuple to hold this row
        PyObject * row = PyTuple_New(fields); 
        // iterate over the data fields
        for (int field = 0; field < fields; field++) {
            // place holder for the field value
            const char * value = "";
            // if it is not null
            if (!PQgetisnull(result, tuple, field)) {
                // extract it
                value = PQgetvalue(result, tuple, field);
            }
            // convert it into a python string
            PyObject * item = PyUnicode_FromString(value);
            // add it to the tuple
            PyTuple_SET_ITEM(row, field, item);
        }
        // and now that the row tuple is fully built, add it to the data set
        PyTuple_SET_ITEM(data, tuple+1, row);
    }

    // return the data tuple
    return data;
}


// analyze and process the result set
PyObject *
pyre::extensions::postgres::
processResult(string_t command, PGresult * result, resultProcessor_t processor)
{
    // in case someone is listening...
    pyre::journal::debug_t debug("postgres.execution");
    debug 
        << pyre::journal::at(__HERE__)
        << "analyzing result set"
        << pyre::journal::endl;

    //  this is what we will return to the caller
    PyObject * value;
    // start looking
    if (!result) {
        // a null result signifies that there is nothing available from the server this can
        // happen when repeatedly calling {retrieve} to get the result of queries that contain
        // multiple SQL statements; it is not necessarily and error

        // return None
        Py_INCREF(Py_None);
        value = Py_None;

    } else if (PQresultStatus(result) == PGRES_COMMAND_OK) {
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
        value = processor(result);
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
