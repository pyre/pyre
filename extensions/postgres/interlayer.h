// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_postgres_interlayer_h)
#define pyre_extensions_postgres_interlayer_h


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace postgres {

            // types
            typedef const char * const string_t;

            // other utilities
            PyObject * resultTuples(PGresult *);

            // exceptions
            PyObject * raiseOperationalError(string_t description);
            PyObject * raiseProgrammingError(string_t description, string_t command);

        } // of namespace postgres
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
