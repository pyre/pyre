// -*- C++ -*-
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                              Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005 All Rights Reserved
//
// <LicenseText>
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <portinfo>
#include <Python.h>
#include <pyre/mpi.h>

#if 0
#include "journal/debug.h"
#endif

#include "constants.h"
#include "ports.h"
#include "exceptions.h"

// send a string
const char * const
pyre::extensions::mpi::
sendString__name__ = "sendString";

const char * const
pyre::extensions::mpi::
sendString__doc__ = "send a string to another process";

PyObject * 
pyre::extensions::mpi::
sendString(PyObject *, PyObject * args)
{
    // placeholder for the arguments
    int tag;
    int len;
    int peer;
    char * str;
    PyObject * py_comm;

    // extract the arguments from the tuple
    if (!PyArg_ParseTuple(
                          args,
                          "O!iis#:sendString",
                          &PyCapsule_Type, &py_comm,
                          &peer, &tag,
                          &str, &len)) {
        return 0;
    }

    // check that we were handed the correct kind of communicator capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // convert into the pyre::mpi object
    communicator_t * comm = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

#if 0
    // dump arguments
    journal::debug_t info("mpi.ports");
    info
        << journal::at(__HERE__)
        << "peer={" << peer
        << "}, tag={" << tag
        << "}, string={" << str << "}@" << len
        << journal::endl;
#endif

    // send the length of the string
    int status = MPI_Send(&len, 1, MPI_INT, peer, tag, comm->handle());

    // send the data (along with the terminating null)
    status = MPI_Send(str, len+1, MPI_CHAR, peer, tag, comm->handle());

    // return
    Py_INCREF(Py_None);
    return Py_None;
}


// receive a string
const char * const
pyre::extensions::mpi::
receiveString__doc__ = "";

const char * const
pyre::extensions::mpi::
receiveString__name__ = "receiveString";

PyObject *
pyre::extensions::mpi::
receiveString(PyObject *, PyObject * args)
{
    // placeholders for the arguments
    int tag;
    int peer;
    PyObject * py_comm;

    // extract the arguments from the tuple
    if (!PyArg_ParseTuple(
                          args,
                          "O!ii:receiveString",
                          &PyCapsule_Type, &py_comm,
                          &peer, &tag)) {
        return 0;
    }

    // check that we were handed the correct kind of communicator capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // convert into the pyre::mpi object
    communicator_t * comm = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

    // receive the length
    int len;
    MPI_Status status;
    MPI_Recv(&len, 1, MPI_INT, peer, tag, comm->handle(), &status);

    // receive the data
    char * str = new char[len+1];
    MPI_Recv(str, len+1, MPI_CHAR, peer, tag, comm->handle(), &status);

#if 0
    // dump message
    journal::debug_t info("mpi.ports");
    info
        << journal::at(__HERE__)
        << "peer={" << peer
        << "}, tag={" << tag
        << "}, string={" << str << "}@" << len
        << journal::endl;
#endif

    // build the return value
    PyObject * value = Py_BuildValue("s", str);

    // clean up
    delete [] str;

    // return
    return value;
}


// end of file
