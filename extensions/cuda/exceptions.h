// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

#if !defined(pyre_extensions_cuda_exceptions_h)
#define pyre_extensions_cuda_exceptions_h


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace cuda {

            // exception registration
            PyObject * registerExceptionHierarchy(PyObject *);

            // base class for cuda errors
            extern PyObject * Error;
            extern const char * const Error__name__;

        } // of namespace cuda
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
