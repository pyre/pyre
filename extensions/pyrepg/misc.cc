// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

#include "misc.h"


// copyright
static char pypyrepg_copyright_note[] = 
    "pyrepg: (c) 1998-2011 Michael A.G. Aïvázis";


PyObject * pypyrepg_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pypyrepg_copyright_note);
}
    
// version
static char pypyrepg_version_string[] = 
    "1.0";


PyObject * pypyrepg_version(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pypyrepg_version_string);
}
    
// end of file
