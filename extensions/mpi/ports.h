// -*- C++ -*-
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                              Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005 All Rights Reserved
//
// <LicenseText>
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#if !defined(pyre_extensions_mpi_ports_h)
#define pyre_extensions_mpi_ports_h

// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace mpi {

            // send a string
            extern const char * const sendString__name__;
            extern const char * const sendString__doc__;
            PyObject * sendString(PyObject *, PyObject *);

            // receive a string
            extern const char * const receiveString__name__;
            extern const char * const receiveString__doc__;
            PyObject * receiveString(PyObject *, PyObject *);

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
