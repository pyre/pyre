// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_postgres_execute_h)
#define pyre_extensions_postgres_execute_h

namespace pyre {
    namespace extensions {
        namespace postgres {

            // establish a connection to the pg back end
            const char * const execute__name__ = "execute";
            const char * const execute__doc__ = "execute a single command";
            PyObject * execute(PyObject *, PyObject *);

        } // of namespace postgres
    } // of namespace extensions
} // of namespace pyre

# endif

// end of file
