// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <pyre/journal.h>

#include "tests.h"

// typedefs
typedef pyre::journal::debug_t debug_t;
typedef pyre::journal::firewall_t firewall_t;
typedef pyre::journal::info_t info_t;
typedef pyre::journal::warning_t warning_t;
typedef pyre::journal::error_t error_t;


// debug
PyObject * 
pyre::extensions::journal::
debugTest(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:debugTest", &name)) {
        return 0;
    }

    // build the channel
    debug_t debug(name);

    // say something
    debug 
        << pyre::journal::at(__HERE__)
        << "hello from C++"
        << pyre::journal::endl;

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// firewall
PyObject * 
pyre::extensions::journal::
firewallTest(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:firewallTest", &name)) {
        return 0;
    }

    // build the channel
    firewall_t firewall(name);

    // say something
    firewall 
        << pyre::journal::at(__HERE__)
        << "hello from C++"
        << pyre::journal::endl;

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// info
PyObject * 
pyre::extensions::journal::
infoTest(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:infoTest", &name)) {
        return 0;
    }

    // build the channel
    info_t info(name);

    // say something
    info 
        << pyre::journal::at(__HERE__)
        << "hello from C++"
        << pyre::journal::endl;

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// warning
PyObject * 
pyre::extensions::journal::
warningTest(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:warningTest", &name)) {
        return 0;
    }

    // build the channel
    warning_t warning(name);

    // say something
    warning 
        << pyre::journal::at(__HERE__)
        << "hello from C++"
        << pyre::journal::endl;

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// error
PyObject * 
pyre::extensions::journal::
errorTest(PyObject *, PyObject * args)
{
    // storage for the name of the channel
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:errorTest", &name)) {
        return 0;
    }

    // build the channel
    error_t error(name);

    // say something
    error 
        << pyre::journal::at(__HERE__)
        << "hello from C++"
        << pyre::journal::endl;

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}


// end of file
