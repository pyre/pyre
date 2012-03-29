// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <pyre/mpi.h>

#include <pyre/journal.h>

#include "capsules.h"
#include "ports.h"
#include "exceptions.h"

// send a string
const char * const mpi::port::sendString__name__ = "sendString";
const char * const mpi::port::sendString__doc__ = "send a string to another process";

PyObject * mpi::port::sendString(PyObject *, PyObject * args)
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
    if (!PyCapsule_IsValid(py_comm, mpi::communicator::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // convert into the pyre::mpi object
    pyre::mpi::communicator_t * comm = 
        static_cast<pyre::mpi::communicator_t *>
        (PyCapsule_GetPointer(py_comm, mpi::communicator::capsule_t));

    // dump arguments
    pyre::journal::debug_t info("mpi.ports");
    info
        << pyre::journal::at(__HERE__)
        << "peer={" << peer
        << "}, tag={" << tag
        << "}, string={" << str << "}@" << len
        << pyre::journal::endl;

    // send the length of the string
    int status = MPI_Send(&len, 1, MPI_INT, peer, tag, comm->handle());

    // send the data (along with the terminating null)
    status = MPI_Send(str, len+1, MPI_CHAR, peer, tag, comm->handle());

    // return
    Py_INCREF(Py_None);
    return Py_None;
}


// receive a string
const char * const mpi::port::receiveString__doc__ = "";
const char * const mpi::port::receiveString__name__ = "receiveString";

PyObject * mpi::port::receiveString(PyObject *, PyObject * args)
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
    if (!PyCapsule_IsValid(py_comm, mpi::communicator::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // convert into the pyre::mpi object
    pyre::mpi::communicator_t * comm = 
        static_cast<pyre::mpi::communicator_t *>
        (PyCapsule_GetPointer(py_comm, mpi::communicator::capsule_t));

    // receive the length
    int len;
    MPI_Status status;
    MPI_Recv(&len, 1, MPI_INT, peer, tag, comm->handle(), &status);

    // receive the data
    char * str = new char[len+1];
    MPI_Recv(str, len+1, MPI_CHAR, peer, tag, comm->handle(), &status);

    // dump message
    pyre::journal::debug_t info("mpi.ports");
    info
        << pyre::journal::at(__HERE__)
        << "peer={" << peer
        << "}, tag={" << tag
        << "}, string={" << str << "}@" << len
        << pyre::journal::endl;

    // build the return value
    PyObject * value = Py_BuildValue("s", str);

    // clean up
    delete [] str;

    // return
    return value;
}

// end of file
