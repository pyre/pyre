// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(pyre_extensions_mpi_ports_h)
#define pyre_extensions_mpi_ports_h

// place everything in my private namespace
namespace mpi {
    namespace port {

        // send a string
        extern const char * const sendString__name__;
        extern const char * const sendString__doc__;
        PyObject * sendString(PyObject *, PyObject *);

        // receive a string
        extern const char * const receiveString__name__;
        extern const char * const receiveString__doc__;
        PyObject * receiveString(PyObject *, PyObject *);

    } // of namespace port
} // of namespace mpi

#endif

// end of file
