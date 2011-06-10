// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// the module method declarations
#include "connection.h"
#include "exceptions.h"
#include "execute.h"
#include "metadata.h"

// put everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace postgres {

            // the module method table
            PyMethodDef methods[] = {
                // module metadata
                // the copyright method
                { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
                // the version method
                { version__name__, version, METH_VARARGS, version__doc__ },

                // exceptions
                { registerExceptions__name__, 
                  registerExceptions, METH_VARARGS, registerExceptions__doc__ },

                // connections
                { connect__name__, connect, METH_VARARGS, connect__doc__ },
                { disconnect__name__, disconnect, METH_VARARGS, disconnect__doc__ },

                // SQL command execution
                { execute__name__, execute, METH_VARARGS, execute__doc__ },

                // sentinel
                {0, 0, 0, 0}
            };


            // the module documentation string
            const char * const doc = "provides access to PostgreSQL databases";

            // the module definition structure
            PyModuleDef module = {
                // header
                PyModuleDef_HEAD_INIT,
                // the name of the module
                "postgres",
                // the module documentation string
                doc,
                // size of the per-interpreter state of the module; -1 if this state is global
                -1,
                // the methods defined in this module
                methods
            };

        } // of namespace postgres
    } // of namespace extensions
} // of namespace pyre


// initialization function for the module
// *must* be called PyInit_postgres
PyMODINIT_FUNC
PyInit_postgres()
{
    // create the module
    PyObject * module = PyModule_Create(&pyre::extensions::postgres::module);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return module;
    }
    // and return the newly created module
    return module;
}


// end of file
