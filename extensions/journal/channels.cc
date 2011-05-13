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

// typedefs
typedef pyre::journal::debug_t debug_t;
typedef pyre::journal::firewall_t firewall_t;
typedef pyre::journal::info_t info_t;
typedef pyre::journal::warning_t warning_t;
typedef pyre::journal::error_t error_t;

// capsule names
static const char * debugInventoryCapsuleName = "debugInventory";
static const char * firewallInventoryCapsuleName = "firewallInventory";
static const char * infoInventoryCapsuleName = "infoInventory";
static const char * warningInventoryCapsuleName = "warningInventory";
static const char * errorInventoryCapsuleName = "errorInventory";


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


// firewallLookup
PyObject * 
pyre::extensions::journal::
firewallLookup(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return 0;
    }
    // access the state
    firewall_t::inventory_t * inventory = &firewall_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, firewallInventoryCapsuleName, 0);
}


// firewallSet
PyObject * 
pyre::extensions::journal::
firewallSet(PyObject *, PyObject * args)
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
    firewall_t::inventory_t * inventory =
        static_cast<firewall_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, firewallInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// firewallGet
PyObject * 
pyre::extensions::journal::
firewallGet(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    firewall_t::inventory_t * inventory =
        static_cast<firewall_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, firewallInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// infoLookup
PyObject * 
pyre::extensions::journal::
infoLookup(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return 0;
    }
    // access the state
    info_t::inventory_t * inventory = &info_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, infoInventoryCapsuleName, 0);
}


// infoSet
PyObject * 
pyre::extensions::journal::
infoSet(PyObject *, PyObject * args)
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
    info_t::inventory_t * inventory =
        static_cast<info_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, infoInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// infoGet
PyObject * 
pyre::extensions::journal::
infoGet(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    info_t::inventory_t * inventory =
        static_cast<info_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, infoInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// warningLookup
PyObject * 
pyre::extensions::journal::
warningLookup(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return 0;
    }
    // access the state
    warning_t::inventory_t * inventory = &warning_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, warningInventoryCapsuleName, 0);
}


// warningSet
PyObject * 
pyre::extensions::journal::
warningSet(PyObject *, PyObject * args)
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
    warning_t::inventory_t * inventory =
        static_cast<warning_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, warningInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// warningGet
PyObject * 
pyre::extensions::journal::
warningGet(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    warning_t::inventory_t * inventory =
        static_cast<warning_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, warningInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// errorLookup
PyObject * 
pyre::extensions::journal::
errorLookup(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return 0;
    }
    // access the state
    error_t::inventory_t * inventory = &error_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, errorInventoryCapsuleName, 0);
}


// errorSet
PyObject * 
pyre::extensions::journal::
errorSet(PyObject *, PyObject * args)
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
    error_t::inventory_t * inventory =
        static_cast<error_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, errorInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// errorGet
PyObject * 
pyre::extensions::journal::
errorGet(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    error_t::inventory_t * inventory =
        static_cast<error_t::inventory_t *>
        (PyCapsule_GetPointer(inventoryCapsule, errorInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// end of file
