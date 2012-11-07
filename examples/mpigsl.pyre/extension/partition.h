// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(mpigsl_partition_h)
#define mpigsl_partition_h


// place everything in my private namespace
namespace mpigsl {

    // copyright note
    extern const char * const gather__name__;
    extern const char * const gather__doc__;
    PyObject * gather(PyObject *, PyObject *);

    // version
    extern const char * const scatter__name__;
    extern const char * const scatter__doc__;
    PyObject * scatter(PyObject *, PyObject *);

} // of namespace mpigsl

#endif

// end of file
