// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//

#include <portinfo>
#include <Python.h>

#include "metadata.h"


// copyright
PyObject *
pyre::extensions::host::
copyright(PyObject *, PyObject *)
{
    const char * const copyright_note = "host: (c) 1998-2023 Michael A.G. Aïvázis";
    return Py_BuildValue("s", copyright_note);
}


// version
PyObject *
pyre::extensions::host::
version(PyObject *, PyObject *)
{
    const char * const version_string = "1.0";
    return Py_BuildValue("s", version_string);
}


// end of file
