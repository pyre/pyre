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

#include "connection.h"


// establish a new connection
PyObject * pyrepg::connect(PyObject *, PyObject * args) {

    // establish a connection
    PGconn * connection = PQconnectdb("dbname=pyrepg");
    // check
    if (PQstatus(connection) != CONNECTION_OK) {
        return 0;
    }

    return PyCapsule_New(connection, "pyrepg.connection", pyrepg::disconnect);
}


// shutdown an existing connection
void pyrepg::disconnect(PyObject * capsule) {
    // get pointer from the capsule and cast it to a pg connection
    PGconn * connection =
        static_cast<PGconn *>(PyCapsule_GetPointer(capsule, "pyrepg.connection"));
    // shutdown 
    PQfinish(connection);

    // all done
    return;
}


// end of file
