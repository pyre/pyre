// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <iostream>
#include <Python.h>
#include <pyre/journal.h>

#include "init.h"
#include "DefaultDevice.h"

using namespace pyre::extensions::journal;


// initialize
PyObject * 
pyre::extensions::journal::
initialize(PyObject *, PyObject * args)
{
    // accept one argument
    PyObject * channel; // the class that keeps a reference to the default device
    // extract it from the argument tuple
    if (!PyArg_ParseTuple(args, "O:initialize", &channel)) {
        return 0;
    }

    // build a new device handler
    DefaultDevice * device = new DefaultDevice(channel);
    
    // attach it as the default device
    pyre::journal::Chronicler::defaultDevice(device);

    // and return
    Py_INCREF(Py_None);
    return Py_None;
}
    

// end of file
