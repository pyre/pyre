// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_postgres_connection_h)
#define pyre_extensions_postgres_connection_h

namespace pyre {
    namespace extensions {
        namespace postgres {

            // establish a connection to the pg back end
            const char * const connect__name__ = "connect";
            const char * const connect__doc__ = "establish a connection to the postgres back end";
            PyObject * connect(PyObject *, PyObject *);

            // disconnect from the back end
            const char * const disconnect__name__ = "disconnect";
            const char * const disconnect__doc__ = "shut down a connection to the postgres back end";
            PyObject * disconnect(PyObject *, PyObject *);

            void finish(PyObject *);

        } // of namespace postgres
    } // of namespace extensions
} // of namespace pyre


# endif

// end of file
