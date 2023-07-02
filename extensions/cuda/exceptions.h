// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//

#if !defined(pyre_extensions_cuda_exceptions_h)
#define pyre_extensions_cuda_exceptions_h


// place everything in my private namespace
namespace pyre::extensions::cuda {

    // exceptions
    extern PyObject * Error;

    // exception registration
    extern const char * const registerExceptions__name__;
    extern const char * const registerExceptions__doc__;
    PyObject * registerExceptions(PyObject *, PyObject *);

} // namespace pyre::extensions::cuda

#endif

// end of file
