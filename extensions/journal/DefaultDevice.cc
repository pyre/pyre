// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 


// for the build system
#include <portinfo>

// external packages
#include <Python.h>
#include <pyre/journal.h>

// my class header
#include "DefaultDevice.h"


// interface
void
pyre::extensions::journal::DefaultDevice::
record(entry_t & entry, metadata_t & metadata)
{
    // all done
    return;
}


// destructor
pyre::extensions::journal::DefaultDevice::
~DefaultDevice()
{
    Py_DECREF(_owner);
}


// end of file
