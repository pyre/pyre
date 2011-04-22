// -*- C++ -*-
//
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <pyre/mpi.h>

#if 0
#include "journal/debug.h"
#endif

#include "constants.h"
#include "groups.h"
#include "exceptions.h"

// the predefined groups
PyObject *
pyre::extensions::mpi::nullGroup = PyCapsule_New(group_t::null, groupCapsuleName, 0);

PyObject *
pyre::extensions::mpi::emptyGroup = PyCapsule_New(group_t::empty, groupCapsuleName, 0);


// create a communicator group (MPI_Comm_group)
const char * const
pyre::extensions::mpi::
groupCreate__name__ = "groupCreate";

const char * const
pyre::extensions::mpi::
groupCreate__doc__ = "create a communicator group";

PyObject *
pyre::extensions::mpi::
groupCreate(PyObject *, PyObject * args)
{
    // placeholder for the python object
    PyObject * py_comm;

    // extract the communicator from the argument tuple
    if (!PyArg_ParseTuple(args, "O!:groupCreate", &PyCapsule_Type, &py_comm)) {
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

    // build the associated group
    group_t * group = group_t::newGroup(*comm);

    if (!group) {
        PyErr_SetString(PyExc_ValueError, "group could not be created");
        return 0;
    }

    // wrap in a capsule and return the new communicator
    return PyCapsule_New(group, groupCapsuleName, deleteGroup);
}


// return the communicator group size (MPI_Group_size)
const char * const
pyre::extensions::mpi::
groupSize__name__ = "groupSize";

const char * const
pyre::extensions::mpi::
groupSize__doc__ = "retrieve the group size";

PyObject *
pyre::extensions::mpi::
groupSize(PyObject *, PyObject * args)
{
    // placeholder
    PyObject * py_group;

    // parse the argument list
    if (!PyArg_ParseTuple(args, "O!:groupSize", &PyCapsule_Type, &py_group)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_group, groupCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid group");
        return 0;
    }

    // get the group
    group_t * group = 
        static_cast<group_t *>(PyCapsule_GetPointer(py_group, groupCapsuleName));

    // extract the group size and return it
    return PyLong_FromLong(group->size());
}


// return the process rank in a given communicator group (MPI_Group_rank)
const char * const
pyre::extensions::mpi::
groupRank__name__ = "groupRank";

const char * const
pyre::extensions::mpi::
groupRank__doc__ = "retrieve the rank of this process";

PyObject *
pyre::extensions::mpi::
groupRank(PyObject *, PyObject * args)
{
    // placeholder
    PyObject * py_group;

    // parse the argument list
    if (!PyArg_ParseTuple(args, "O!:groupSize", &PyCapsule_Type, &py_group)) {
        return 0;
    }

    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_group, groupCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid group");
        return 0;
    }

    // get the group
    group_t * group = 
        static_cast<group_t *>(PyCapsule_GetPointer(py_group, groupCapsuleName));

    // extract the group size and return it
    return PyLong_FromLong(group->rank());
}


// return the process rank in a given communicator group (MPI_Group_incl)
const char * const
pyre::extensions::mpi::
groupInclude__name__ = "groupInclude";

const char * const
pyre::extensions::mpi::
groupInclude__doc__ = "include processors in this group";

PyObject *
pyre::extensions::mpi::
groupInclude(PyObject *, PyObject * args)
{
    PyObject * py_group;
    PyObject * rankSeq;

    if (!PyArg_ParseTuple(
                          args, 
                          "O!O:groupInclude",
                          &PyCapsule_Type, &py_group,
                          &rankSeq)) {
        return 0;
    }
    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_group, groupCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid group");
        return 0;
    }
    // check the rank sequence
    if (!PySequence_Check(rankSeq)) {
        PyErr_SetString(PyExc_TypeError, "the second argument must be a sequence");
        return 0;
    }

    // get the communicator group
    group_t * group = 
        static_cast<group_t *>(PyCapsule_GetPointer(py_group, groupCapsuleName));

    // store the ranks in a vector
    int size = PySequence_Length(rankSeq);
    int * ranks = new int[size];

    for (int i = 0; i < size; ++i) {
        ranks[i] = PyLong_AsLong(PySequence_GetItem(rankSeq, i));
    }

    // make the MPI call
    group_t * newGroup = group->include(size, ranks);

    // clean up
    delete [] ranks;

    // check that the new group is not a null pointer
    if (!newGroup) {
        PyErr_SetString(Error, "could not build process group");
        return 0;
    }

    // is it the empty group?
    if (newGroup == group_t::empty) {
        return emptyGroup;
    }
    
    // otherwise, wrap it in a capsule and return it
    return PyCapsule_New(newGroup, groupCapsuleName, deleteGroup);
}


// return the process rank in a given communicator group (MPI_Group_excl)
const char * const
pyre::extensions::mpi::
groupExclude__name__ = "groupExclude";

const char * const 
pyre::extensions::mpi::
groupExclude__doc__ = "exclude processors from this group";

PyObject *
pyre::extensions::mpi::
groupExclude(PyObject *, PyObject * args)
{
    PyObject * py_group;
    PyObject * rankSeq;

    if (!PyArg_ParseTuple(
                          args, 
                          "O!O:groupExclude",
                          &PyCapsule_Type, &py_group,
                          &rankSeq)) {
        return 0;
    }
    // check that we were handed the correct kind of capsule
    if (!PyCapsule_IsValid(py_group, groupCapsuleName)) {
        PyErr_SetString(PyExc_TypeError, "the first argument must be a valid group");
        return 0;
    }
    // check the rank sequence
    if (!PySequence_Check(rankSeq)) {
        PyErr_SetString(PyExc_TypeError, "the second argument must be a sequence");
        return 0;
    }

    // get the communicator group
    group_t * group = 
        static_cast<group_t *>(PyCapsule_GetPointer(py_group, groupCapsuleName));

    // store the ranks in a vector
    int size = PySequence_Length(rankSeq);
    int * ranks = new int[size];

    for (int i = 0; i < size; ++i) {
        ranks[i] = PyLong_AsLong(PySequence_GetItem(rankSeq, i));
    }

    // make the MPI call
    group_t * newGroup = group->exclude(size, ranks);

    // clean up and return
    delete [] ranks;

    if (!newGroup) {
        PyErr_SetString(Error, "could not build process group");
        return 0;
    }

    return PyCapsule_New(newGroup, groupCapsuleName, deleteGroup);
}


// helpers
void
pyre::extensions::mpi::
deleteGroup(PyObject * py_group)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(py_group, groupCapsuleName)) {
        return;
    }
    // get the pointer
    group_t * group = 
        static_cast<group_t *>(PyCapsule_GetPointer(py_group, groupCapsuleName));

#if 0
    journal::debug_t info("mpi.fini");
    info
        << journal::at(__HERE__)
        << "group@" << group << ": deleting"
        << journal::endl;
#endif
    // delete it
    delete group;
    // and return
    return;
}

// end of file
