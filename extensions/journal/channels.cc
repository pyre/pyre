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

typedef pyre::journal::Inventory<true> enabled_t;
typedef pyre::journal::Inventory<false> disabled_t;

// capsule names
static const char * enabledInventoryCapsuleName = "enabledInventory";
static const char * disabledInventoryCapsuleName = "disabledInventory";

// lookupDebug
PyObject * 
pyre::extensions::journal::
lookupDebug(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:lookupDebugInventory", &name)) {
        return 0;
    }
    // access the state
    disabled_t * inventory = &debug_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, disabledInventoryCapsuleName, 0);
}


// firewallLookup
PyObject * 
pyre::extensions::journal::
lookupFirewall(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:lookupFirewallInventory", &name)) {
        return 0;
    }
    // access the state
    enabled_t * inventory = &firewall_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, enabledInventoryCapsuleName, 0);
}


// infoLookup
PyObject * 
pyre::extensions::journal::
lookupInfo(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:lookupInfoInventory", &name)) {
        return 0;
    }
    // access the state
    disabled_t * inventory = &info_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, disabledInventoryCapsuleName, 0);
}


// warningLookup
PyObject * 
pyre::extensions::journal::
lookupWarning(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:lookupWarningInventory", &name)) {
        return 0;
    }
    // access the state
    enabled_t * inventory = &warning_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, enabledInventoryCapsuleName, 0);
}


// errorLookup
PyObject * 
pyre::extensions::journal::
lookupError(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:lookupErrorInventory", &name)) {
        return 0;
    }
    // access the state
    enabled_t * inventory = &error_t::lookup(name);
    // encapsulate it and return it
    return PyCapsule_New(inventory, enabledInventoryCapsuleName, 0);
}


// setEnabledState
PyObject * 
pyre::extensions::journal::
setEnabledState(PyObject *, PyObject * args)
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
    enabled_t * inventory =
        static_cast<enabled_t *>
        (PyCapsule_GetPointer(inventoryCapsule, enabledInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// getEnabledState
PyObject * 
pyre::extensions::journal::
getEnabledState(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    enabled_t * inventory =
        static_cast<enabled_t *>
        (PyCapsule_GetPointer(inventoryCapsule, enabledInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// setDisabledState
PyObject * 
pyre::extensions::journal::
setDisabledState(PyObject *, PyObject * args)
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
    disabled_t * inventory =
        static_cast<disabled_t *>
        (PyCapsule_GetPointer(inventoryCapsule, disabledInventoryCapsuleName));
    // adjust the state
    if (state == Py_True) {
        inventory->activate();
    } else {
        inventory->deactivate();
    }

    Py_INCREF(Py_None);
    return Py_None;
}


// getDisabledState
PyObject * 
pyre::extensions::journal::
getDisabledState(PyObject *, PyObject * args)
{
    // accept one parameters
    PyObject * inventoryCapsule;
    // extract it
    if (!PyArg_ParseTuple(args, "O!", &PyCapsule_Type, &inventoryCapsule)) {
        return 0;
    }
    // decapsulate the inventory
    disabled_t * inventory =
        static_cast<disabled_t *>
        (PyCapsule_GetPointer(inventoryCapsule, disabledInventoryCapsuleName));
    // adjust the state
    if (inventory->state()) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// end of file
