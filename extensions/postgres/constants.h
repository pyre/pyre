// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2024 all rights reserved
//

#if !defined(pyre_extensions_postgres_constants_h)
#define pyre_extensions_postgres_constants_h

// local additions to the namespace
namespace pyre { namespace extensions { namespace postgres {
    // the name of the connection capsule
    extern const char * const connectionCapsuleName;

    // exception hierarchy for postgres errors
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

}}} // namespace pyre::extensions::postgres


#endif

// end of file
