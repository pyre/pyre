// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2024 all rights reserved
//

#if !defined(pyre_extensions_postgres_metadata_h)
#define pyre_extensions_postgres_metadata_h


// place everything in my private namespace
namespace pyre { namespace extensions { namespace postgres {

    // copyright note
    extern const char * const copyright__name__;
    extern const char * const copyright__doc__;
    PyObject * copyright(PyObject *, PyObject *);

    // version string
    extern const char * const version__name__;
    extern const char * const version__doc__;
    PyObject * version(PyObject *, PyObject *);

}}} // namespace pyre::extensions::postgres

#endif

// end of file
