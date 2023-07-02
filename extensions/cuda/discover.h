// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//

#if !defined(pyre_extensions_cuda_discover_h)
#define pyre_extensions_cuda_discover_h


// place everything in my private namespace
namespace pyre::extensions::cuda {

    // discover
    const char * const discover__name__ = "discover";
    const char * const discover__doc__ = "device discovery";
    PyObject * discover(PyObject *, PyObject *);

} // namespace pyre::extensions::cuda

#endif

// end of file
