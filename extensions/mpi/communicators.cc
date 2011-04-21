// -*- C++ -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <pyre/mpi.h>

// #include "journal/debug.h"

#include "constants.h"
#include "communicators.h"
#include "exceptions.h"

// helpers
// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace mpi {
            // destructors
            void deleteCommunicator(PyObject *);

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre


using namespace pyre::extensions::mpi;


// create a communicator (MPI_Comm_create)
const char * const 
pyre::extensions::mpi::
communicatorCreate__name__ = "communicatorCreate";

const char * const 
pyre::extensions::mpi::
communicatorCreate__doc__ = "create a communicator";

PyObject *
pyre::extensions::mpi::
communicatorCreate(PyObject *, PyObject * args)
{
    // placeholders for the python objects
    PyObject * py_old;
    PyObject * py_group;

    // extract them from the argument tuple in a type safe manner
    if (!PyArg_ParseTuple(
                          args,
                          "O!O!:communicatorCreate",
                          &PyCapsule_Type, &py_old, &PyCapsule_Type, &py_group)) {
        return 0;
    }
    // check that we were handed the correct kind of communicator capsule
    if (!PyCapsule_IsValid(py_old, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }
    // check that we were handed the correct kind of group capsule
    if (!PyCapsule_IsValid(py_group, groupCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the second argument must be a valid communicator group");
        return 0;
    }

    // convert into the pyre::mpi objects
    communicator_t * old = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_old, communicatorCapsuleName));
    group_t * group =
        static_cast<group_t *>(PyCapsule_GetPointer(py_group, groupCapsuleName));

    // allocate a new communicator
    communicator_t * comm = old->newCommunicator(*group);

    // if the allocation failed
    if (!comm) {
        // bail out
        PyErr_SetString(Error, "communicator could not be created");
        return 0;
    }

    // wrap in a capsule and return the new communicator
    return PyCapsule_New(comm, communicatorCapsuleName, deleteCommunicator);
}

// create a cartesian communicator (MPI_Cart_create)
const char * const
pyre::extensions::mpi::
communicatorCreateCartesian__name__ = "communicatorCreateCartesian";

const char * const
pyre::extensions::mpi::
communicatorCreateCartesian__doc__ = "create a Cartesian communicator";

PyObject *
pyre::extensions::mpi::
communicatorCreateCartesian(PyObject *, PyObject * args)
{
    // placeholders for the argument list
    int reorder;
    PyObject * py_comm;
    PyObject * procSeq;
    PyObject * periodSeq;

#if 0
    journal::debug_t info("mpi.cartesian");
#endif

    // extract them from the argument tuple
    if (!PyArg_ParseTuple(
                          args, 
                          "O!iOO:communicatorCreateCartesian",
                          &PyCapsule_Type, &py_comm,
                          &reorder, &procSeq, &periodSeq)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }
    // check the processor sequence
    if (!PySequence_Check(procSeq)) {
        PyErr_SetString(PyExc_TypeError, "the third argument must be a sequence");
        return 0;
    }
    // check the period sequence
    if (!PySequence_Check(periodSeq)) {
        PyErr_SetString(PyExc_TypeError, "the fourth argument must be a sequence");
        return 0;
    }

    // get the communicator
    communicator_t * comm = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

    // compute the dimensionality of the communicator
    int size = PySequence_Size(procSeq);
    if (size != PySequence_Size(periodSeq)) {
        PyErr_SetString(Error, "mismatch in size of processor and period lists");
        return 0;
    }

#if 0
    info << journal::at(__HERE__) << "dimension = " << size << journal::newline;
#endif

    // allocate the arrays for the MPI call
    int * procs = new int[size];
    int * periods = new int[size];

    // copy the data over
#if 0
    info << journal::at(__HERE__) << "axes: ";
#endif
    for (int dim = 0; dim < size; ++dim) {
        procs[dim] = PyLong_AsLong(PySequence_GetItem(procSeq, dim));
        periods[dim] = PyLong_AsLong(PySequence_GetItem(periodSeq, dim));
#if 0
        info << " (" << procs[dim] << "," << periods[dim] << ")";
#endif
    }
#if 0
    info << journal::endl;
#endif

    // make the MPI call
    communicator_t * cartesian = comm->cartesian(size, procs, periods, reorder);
#if 0
    info
        << journal::at(__HERE__)
        << "created cartesian@" << cartesian << " from comm@" << comm
        << journal::endl;
#endif

// clean up and return
    delete [] procs;
    delete [] periods;

    if (!cartesian) {
        PyErr_SetString(Error, "could not build cartesian communicator");
        return 0;
    }

    // return the new communicator
    return PyCapsule_New(cartesian, communicatorCapsuleName, deleteCommunicator);
}


// return the communicator size (MPI_Comm_size)
const char * const
pyre::extensions::mpi::
communicatorSize__name__ = "communicatorSize";

const char * const
pyre::extensions::mpi::
communicatorSize__doc__ = "get the size of a communicator";

PyObject *
pyre::extensions::mpi::
communicatorSize(PyObject *, PyObject * args)
{
    // placeholder
    PyObject * py_comm;

    // parse the argument list
    if (!PyArg_ParseTuple(args, "O!:communicatorSize", &PyCapsule_Type, &py_comm)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // get the communicator
    communicator_t * comm = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

    // extract the communicator size and return it
    return PyLong_FromLong(comm->size());
}


// return the communicator rank (MPI_Comm_rank)
const char * const
pyre::extensions::mpi::
communicatorRank__name__ = "communicatorRank";

const char * const
pyre::extensions::mpi::
communicatorRank__doc__ = "get the rank of this process in the given communicator";

PyObject *
pyre::extensions::mpi::
communicatorRank(PyObject *, PyObject * args)
{
    // placeholder
    PyObject * py_comm;

    // parse the argument list
    if (!PyArg_ParseTuple(args, "O!:communicatorRank", &PyCapsule_Type, &py_comm)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // get the communicator
    communicator_t * comm = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

    // return
    return PyLong_FromLong(comm->rank());
}


// set a communicator barrier (MPI_Barrier)
const char * const
pyre::extensions::mpi::
communicatorBarrier__name__ = "communicatorBarrier";

const char * const 
pyre::extensions::mpi::
communicatorBarrier__doc__ = "block until all members of this communicator reach this point";

PyObject *
pyre::extensions::mpi::
communicatorBarrier(PyObject *, PyObject * args)
{
    // placeholder
    PyObject * py_comm;

    // parse the argument list
    if (!PyArg_ParseTuple(args, "O!:communicatorBarrier", &PyCapsule_Type, &py_comm)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // get the communicator
    communicator_t * comm = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

    // set up the barrier
    comm->barrier();

    // and return
    Py_INCREF(Py_None);
    return Py_None;

}


// return the coordinates of the process in the cartesian communicator (MPI_Cart_coords)
const char * const
pyre::extensions::mpi::
communicatorCartesianCoordinates__name__ = "communicatorCartesianCoordinates";

const char * const 
pyre::extensions::mpi::
communicatorCartesianCoordinates__doc__ = "retrieve the cartesian coordinates of this process";

PyObject *
pyre::extensions::mpi::
communicatorCartesianCoordinates(PyObject *, PyObject * args)
{
    // placeholders
    int dim;
    int rank;
    PyObject * py_comm;

    // parse the argument list
    if (!PyArg_ParseTuple(
                          args,
                          "O!ii:communicatorCartesianCoordinates",
                          &PyCapsule_Type, &py_comm,
                          &rank, &dim)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_comm, communicatorCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid communicator");
        return 0;
    }

    // get the communicator
    communicator_t * cartesian = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(py_comm, communicatorCapsuleName));

    // allocate room for the coordinates
    int * coordinates = new int[dim];
    for (int i=0; i<dim; ++i) {
        coordinates[i] = 0;
    }

    // dump
#if 0
    journal::debug_t info("mpi.cartesian");
    if (info.state()) {
        int wr, ws;
        MPI_Comm_rank(MPI_COMM_WORLD, &wr);
        MPI_Comm_size(MPI_COMM_WORLD, &ws);
        info
            << journal::at(__HERE__)
            << "[" << wr << ":" << ws << "] "
            << "communicator@" << cartesian << ": "
            << dim << "-dim cartesian communicator, rank=" << rank
            << journal::newline;
    }
#endif

    cartesian->cartesianCoordinates(rank, dim, coordinates);
#if 0
    info << "coordinates:";
    for (int i=0; i < dim; ++i) {
        info << " " << coordinates[i];
    }
    info << journal::endl;
#endif

    PyObject *value = PyTuple_New(dim);
    for (int i = 0; i < dim; ++i) {
        PyTuple_SET_ITEM(value, i, PyLong_FromLong(coordinates[i]));
    }

    // clean up
    delete [] coordinates;
    
    // and return
    return value;
}


// helpers
void
pyre::extensions::mpi::
deleteCommunicator(PyObject * comm)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(comm, communicatorCapsuleName)) {
        return;
    }
    // get the pointer
    communicator_t * communicator = 
        static_cast<communicator_t *>(PyCapsule_GetPointer(comm, communicatorCapsuleName));

#if 0
    journal::debug_t info("mpi.fini");
    info
        << journal::at(__HERE__)
        << "[" << communicator->rank() << ":" << communicator->size() << "] "
        << "deleting comm@" << communicator
        << journal::endl;
#endif

    delete communicator;

    return;
}

// end of file
