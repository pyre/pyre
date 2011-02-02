// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyrepg_execute_h)
#define pyrepg_execute_h

namespace pyrepg {

    // establish a connection to the pg back end
    const char * const execute__name__ = "execute";
    const char * const execute__doc__ = "execute a single command";
    PyObject * execute(PyObject *, PyObject *);
}

# endif

// end of file
