// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// for the build system
#include <portinfo>
// external dependencies
#include <Python.h>
#include <pyre/mpi.h>

// the module method declarations
#include "constants.h"
#include "communicators.h"
#include "exceptions.h"
#include "groups.h"
#include "metadata.h"
#include "ports.h"
#include "startup.h"


// put everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace mpi {

            // the module method table
            PyMethodDef module_methods[] = {
                // module metadata
                // the copyright method
                { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
                // the version
                { version__name__, version, METH_VARARGS, version__doc__ },

                // init-fini
                { initialize__name__, initialize, METH_VARARGS, initialize__doc__ },
                { finalize__name__, finalize, METH_VARARGS, finalize__doc__ },
        
                // communicators
                { communicatorCreate__name__, 
                  communicatorCreate, METH_VARARGS, communicatorCreate__doc__ },
                { communicatorSize__name__, 
                  communicatorSize, METH_VARARGS, communicatorSize__doc__ },
                { communicatorRank__name__, 
                  communicatorRank, METH_VARARGS, communicatorRank__doc__ },
                { communicatorBarrier__name__, 
                  communicatorBarrier, METH_VARARGS, communicatorBarrier__doc__ },
                { communicatorCreateCartesian__name__, 
                  communicatorCreateCartesian, METH_VARARGS, communicatorCreateCartesian__doc__ },
                { communicatorCartesianCoordinates__name__, 
                  communicatorCartesianCoordinates, METH_VARARGS, 
                  communicatorCartesianCoordinates__doc__ },

                // groups
                { groupCreate__name__, groupCreate, METH_VARARGS, groupCreate__doc__ },
                { groupSize__name__, groupSize, METH_VARARGS, groupSize__doc__ },
                { groupRank__name__, groupRank, METH_VARARGS, groupRank__doc__ },
                { groupInclude__name__, groupInclude, METH_VARARGS, groupInclude__doc__ },
                { groupExclude__name__, groupExclude, METH_VARARGS, groupExclude__doc__ },

                // ports
                { sendString__name__, sendString, METH_VARARGS, sendString__doc__ },
                { receiveString__name__, receiveString, METH_VARARGS, receiveString__doc__ },

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
                "mpi", 
                // the module documentation string
                __doc__,
                // size of the per-interpreter state of the module; -1 if this state is global
                -1,
                // the methods defined in this module
                module_methods
            };

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre


using namespace pyre::extensions::mpi;

// initialization function for the module
// *must* be called PyInit_mpi
PyMODINIT_FUNC
PyInit_mpi()
{
    // create the module
    PyObject * module = PyModule_Create(&pyre::extensions::mpi::module_definition);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return 0;
    }
    // otherwise, we have an initialized module
    pyre::extensions::mpi::registerExceptionHierarchy(module);

    // initialize MPI
    if (!pyre::extensions::mpi::initialize(0, 0)) {
        return 0;
    }

    // add the world communicator
    PyModule_AddObject(module, "world", worldCommunicator);

    // constants
    PyModule_AddObject(module, "undefined", PyLong_FromLong(MPI_UNDEFINED));

    // groups
    // add the null group capsule as a module attribute
    PyModule_AddObject(module, "nullGroup", nullGroup);
    // add the empty group capsule as a module attribute
    PyModule_AddObject(module, "emptyGroup", emptyGroup);

    // and return the newly created module
    return module;
}

// end of file
