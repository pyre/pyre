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

#include "constants.h"
#include "connection.h"

// establish a new connection
PyObject * pyrepg::connect(PyObject *, PyObject * args) {
    // the connection specification
    const char * specification;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:connect", &specification)) {
        return 0;
    }

    // establish a connection
    PGconn * connection = PQconnectdb(specification);
    // check
    if (PQstatus(connection) != CONNECTION_OK) {
        return 0;
    }

    return PyCapsule_New(connection, pyrepg::connectionCapsuleName, pyrepg::finish);
}

PyObject * pyrepg::disconnect(PyObject *, PyObject * args) {
    // the connection capsule
    PyObject * connection;
    // extract it from the arguments
    if (!PyArg_ParseTuple(args, "O!:disconnect", &PyCapsule_Type, &connection)) {
        return 0;
    }
    // call the destructor
    pyrepg::finish(connection);
    // and remove the destructor
    PyCapsule_SetDestructor(connection, 0);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// shutdown an existing connection
void pyrepg::finish(PyObject * capsule) {
    // bail if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, pyrepg::connectionCapsuleName)) {
        return;
    }
    // get pointer from the capsule and cast it to a pg connection
    PGconn * connection =
        static_cast<PGconn *>(PyCapsule_GetPointer(capsule, pyrepg::connectionCapsuleName));
    // shutdown 
    PQfinish(connection);
    // all done
    return;
}


// end of file
