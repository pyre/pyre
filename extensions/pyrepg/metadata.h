// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyrepg_metadata_h)
#define pyrepg_metadata_h


// place everything in my private namespace
namespace pyrepg {

    // copyright note
    const char * const copyright__name__ = "copyright";
    const char * const copyright__doc__ = "the module copyright string";
    PyObject * copyright(PyObject *, PyObject *);

    // version string
    const char * const version__name__ = "version";
    const char * const version__doc__ = "the module version string";
    PyObject * version(PyObject *, PyObject *);

}

#endif

// end of file
