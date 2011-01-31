// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

#include "metadata.h"


// copyright
PyObject * pyrepg::copyright(PyObject *, PyObject *)
{
    const char * const copyright_note = "pyrepg: (c) 1998-2011 Michael A.G. Aïvázis";
    return Py_BuildValue("s", copyright_note);
}
    

// version
PyObject * pyrepg::version(PyObject *, PyObject *)
{
    const char * const version_string = "1.0";
    return Py_BuildValue("s", version_string);
}
    
// end of file
