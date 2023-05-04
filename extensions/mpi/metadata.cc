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
const char * const mpi::copyright__name__ = "copyright";
const char * const mpi::copyright__doc__ = "the module copyright string";
PyObject * mpi::copyright(PyObject *, PyObject *)
{
    const char * const copyright_note = "mpi: (c) 1998-2023 Michael A.G. Aïvázis";
    return Py_BuildValue("s", copyright_note);
}


// version
const char * const mpi::version__name__ = "version";
const char * const mpi::version__doc__ = "the module version string";
PyObject * mpi::version(PyObject *, PyObject *)
{
    const char * const version_string = "0.0";
    return Py_BuildValue("s", version_string);
}


// end of file
