// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(mpigsl_exceptions_h)
#define mpigsl_exceptions_h


// place everything in my private namespace
namespace mpigsl {

    // exception registration
    PyObject * registerExceptionHierarchy(PyObject *);
    
} // of namespace mpigsl

#endif

// end of file
