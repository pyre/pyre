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
            const char * const registerExceptions__name__ = "registerExceptions";
            const char * const registerExceptions__doc__ = 
                "register the classes that represent the standard exceptions raised by"
                "DB API 2.0 compliant implementations";
            PyObject * registerExceptions(PyObject *, PyObject *);

        } // of namespace postgres
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
