// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <pyre/journal.h>

#include "channels.h"

typedef pyre::journal::debug_t debug_t;
static const char * debugInventoryCapsuleName = "debugInventory";


// debugLookup
PyObject * 
pyre::extensions::journal::
debugLookup(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return 0;
    }
    // access the state
    debug_t::inventory_t * inventory = &debug_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, debugInventoryCapsuleName, 0);
}


// debugSet
PyObject * 
pyre::extensions::journal::
debugSet(PyObject *, PyObject * args)
{
    // accept two parameters
    PyObject * state;
    PyObject * inventoryCapsule;
    // extract them
    if (!PyArg_ParseTuple(
                          args, "O!O!",
                          &PyCapsule_Type, &inventoryCapsule,
                          &PyBool_Type, &state)) {
        return 0;
    }
    // decapsulate the inventory
    debug_t::inventory_t * inventory =
        static_cast<debug_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, debugInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// debugGet
PyObject * 
pyre::extensions::journal::
debugGet(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    debug_t::inventory_t * inventory =
        static_cast<debug_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, debugInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}



// end of file
