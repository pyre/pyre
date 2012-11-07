// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(mpigsl_metadata_h)
#define mpigsl_metadata_h


// place everything in my private namespace
namespace mpigsl {

    // copyright note
    extern const char * const copyright__name__;
    extern const char * const copyright__doc__;
    PyObject * copyright(PyObject *, PyObject *);

    // version
    extern const char * const version__name__;
    extern const char * const version__doc__;
    PyObject * version(PyObject *, PyObject *);

} // of namespace mpigsl

#endif

// end of file
