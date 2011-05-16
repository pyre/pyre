// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_journal_tests_h)
#define pyre_extensions_journal_tests_h


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace journal {

            // debug
            const char * const debugTest__name__ = "debugTest";
            const char * const debugTest__doc__ = "test the debug channel";
            PyObject * debugTest(PyObject *, PyObject *);
            // firewall
            const char * const firewallTest__name__ = "firewallTest";
            const char * const firewallTest__doc__ = "test the firewall channel";
            PyObject * firewallTest(PyObject *, PyObject *);
            // info
            const char * const infoTest__name__ = "infoTest";
            const char * const infoTest__doc__ = "test the info channel";
            PyObject * infoTest(PyObject *, PyObject *);
            // warning
            const char * const warningTest__name__ = "warningTest";
            const char * const warningTest__doc__ = "test the warning channel";
            PyObject * warningTest(PyObject *, PyObject *);
            // error
            const char * const errorTest__name__ = "errorTest";
            const char * const errorTest__doc__ = "test the error channel";
            PyObject * errorTest(PyObject *, PyObject *);

        } // of namespace journal
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
