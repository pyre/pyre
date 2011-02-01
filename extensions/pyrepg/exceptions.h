// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyrepg_exceptions_h)
#define pyrepg_exceptions_h


// place everything in my private namespace
namespace pyrepg {

    // exception registration
    const char * const registerExceptions__name__ = "registerExceptions";
    const char * const registerExceptions__doc__ = 
        "register the classes that represent the standard exceptions raised by"
        "DB API 2.0 compliant implementations";
    PyObject * registerExceptions(PyObject *, PyObject *);

} // of namespace pyrepg

#endif

// end of file
