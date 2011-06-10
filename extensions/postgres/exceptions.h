// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_postgres_exceptions_h)
#define pyre_extensions_postgres_exceptions_h


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace postgres {

            // exception registration
            extern const char * const registerExceptions__name__;
            extern const char * const registerExceptions__doc__;
            PyObject * registerExceptions(PyObject *, PyObject *);

        } // of namespace postgres
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
