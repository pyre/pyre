// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_journal_init_h)
#define pyre_extensions_journal_init_h


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace journal {

            // initialization
            const char * const initialize__name__ = "initialize";
            const char * const initialize__doc__ = "the extension initialization";
            PyObject * initialize(PyObject *, PyObject *);

        } // of namespace journal
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
