// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyrepg_constants_h)
#define pyrepg_constants_h

// local additions to the namespace
namespace pyrepg {
    // the name of the connection capsule
    const char * const connectionCapsuleName = "pyrepg.connection";

    // exception hierarchy for pyrepg errors
    extern PyObject * Error;
    extern PyObject * Warning;
    extern PyObject * InterfaceError;
    extern PyObject * DatabaseError;
    extern PyObject * DataError;
    extern PyObject * OperationalError;
    extern PyObject * IntegrityError;
    extern PyObject * InternalError;
    extern PyObject * ProgrammingError;
    extern PyObject * NotSupportedError;

}


# endif

// end of file
