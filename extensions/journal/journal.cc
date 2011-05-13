// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <Python.h>

// the module method declarations
#include "exceptions.h"
#include "metadata.h"
#include "channels.h"


// put everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace journal {

            // the module method table
            PyMethodDef module_methods[] = {
                // the copyright method
                { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
                // the version
                { version__name__, version, METH_VARARGS, version__doc__ },

                // channels
                // debug
                { debugLookup__name__, debugLookup, METH_VARARGS, debugLookup__doc__ },
                { debugSet__name__, debugSet, METH_VARARGS, debugSet__doc__ },
                { debugGet__name__, debugGet, METH_VARARGS, debugGet__doc__ },
                // firewall
                { firewallLookup__name__, firewallLookup, METH_VARARGS, firewallLookup__doc__ },
                { firewallSet__name__, firewallSet, METH_VARARGS, firewallSet__doc__ },
                { firewallGet__name__, firewallGet, METH_VARARGS, firewallGet__doc__ },
                // info
                { infoLookup__name__, infoLookup, METH_VARARGS, infoLookup__doc__ },
                { infoSet__name__, infoSet, METH_VARARGS, infoSet__doc__ },
                { infoGet__name__, infoGet, METH_VARARGS, infoGet__doc__ },
                // warning
                { warningLookup__name__, warningLookup, METH_VARARGS, warningLookup__doc__ },
                { warningSet__name__, warningSet, METH_VARARGS, warningSet__doc__ },
                { warningGet__name__, warningGet, METH_VARARGS, warningGet__doc__ },
                // error
                { errorLookup__name__, errorLookup, METH_VARARGS, errorLookup__doc__ },
                { errorSet__name__, errorSet, METH_VARARGS, errorSet__doc__ },
                { errorGet__name__, errorGet, METH_VARARGS, errorGet__doc__ },
        
                // sentinel
                {0, 0, 0, 0}
            };

            // the module documentation string
            const char * const __doc__ = "sample module documentation string";

            // the module definition structure
            PyModuleDef module_definition = {
                // header
                PyModuleDef_HEAD_INIT,
                // the name of the module
                "journal", 
                // the module documentation string
                __doc__,
                // size of the per-interpreter state of the module; -1 if this state is global
                -1,
                // the methods defined in this module
                module_methods
            };

        } // of namespace journal
    } // of namespace extensions
} // of namespace pyre


// initialization function for the module
// *must* be called PyInit_journal
PyMODINIT_FUNC
PyInit_journal()
{
    // create the module
    PyObject * module = PyModule_Create(&pyre::extensions::journal::module_definition);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return module;
    }
    // otherwise, we have an initialized module
    pyre::extensions::journal::registerExceptionHierarchy(module);

    // and return the newly created module
    return module;
}

// end of file
