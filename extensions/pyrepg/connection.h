// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyrepg_connection_h)
#define pyrepg_connection_h

namespace pyrepg {

    // establish a connection to the pg back end
    const char * const connect__name__ = "connect";
    const char * const connect__doc__ = "establish a connection to the postgres back end";
    PyObject * connect(PyObject *, PyObject *);

}


# endif

// end of file
