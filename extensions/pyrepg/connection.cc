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


PyObject * pyrepg::connect(PyObject *, PyObject * args) {

    // establish a connection
    PGconn * connection = PQconnectdb("dbname=pyrepg");
    // check
    if (PQstatus(connection) != CONNECTION_OK) {
        std::cerr
            << "pyrepg.connect: connection failed: "
            << PQerrorMessage(connection)
            << std::endl;
    }

    return PyCObject_FromVoidPtr(connection, 0);
}


// end of file
