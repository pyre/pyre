// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pyre_extensions_journal_channels_h)
#define pyre_extensions_journal_channels_h


// place everything in my private namespace
namespace pyre {
    namespace extensions {
        namespace journal {

            // lookup a name in the debug index
            const char * const debugLookup__name__ = "debugLookup";
            const char * const debugLookup__doc__ = "get the channel state from the debug index";
            PyObject * debugLookup(PyObject *, PyObject *);

            // manipulate the state of a debug channel
            const char * const debugSet__name__ = "debugSet";
            const char * const debugSet__doc__ = "set the state of a debug channel";
            PyObject * debugSet(PyObject *, PyObject *);

            const char * const debugGet__name__ = "debugGet";
            const char * const debugGet__doc__ = "get the state of a debug channel";
            PyObject * debugGet(PyObject *, PyObject *);

            // lookup a name in the firewall index
            const char * const firewallLookup__name__ = "firewallLookup";
            const char * const firewallLookup__doc__ = 
                "get the channel state from the firewall index";
            PyObject * firewallLookup(PyObject *, PyObject *);

            // manipulate the state of a firewall channel
            const char * const firewallSet__name__ = "firewallSet";
            const char * const firewallSet__doc__ = "set the state of a firewall channel";
            PyObject * firewallSet(PyObject *, PyObject *);

            const char * const firewallGet__name__ = "firewallGet";
            const char * const firewallGet__doc__ = "get the state of a firewall channel";
            PyObject * firewallGet(PyObject *, PyObject *);

            // lookup a name in the info index
            const char * const infoLookup__name__ = "infoLookup";
            const char * const infoLookup__doc__ = "get the channel state from the info index";
            PyObject * infoLookup(PyObject *, PyObject *);

            // manipulate the state of a info channel
            const char * const infoSet__name__ = "infoSet";
            const char * const infoSet__doc__ = "set the state of a info channel";
            PyObject * infoSet(PyObject *, PyObject *);

            const char * const infoGet__name__ = "infoGet";
            const char * const infoGet__doc__ = "get the state of a info channel";
            PyObject * infoGet(PyObject *, PyObject *);

            // lookup a name in the warning index
            const char * const warningLookup__name__ = "warningLookup";
            const char * const warningLookup__doc__ =
                "get the channel state from the warning index";
            PyObject * warningLookup(PyObject *, PyObject *);

            // manipulate the state of a warning channel
            const char * const warningSet__name__ = "warningSet";
            const char * const warningSet__doc__ = "set the state of a warning channel";
            PyObject * warningSet(PyObject *, PyObject *);

            const char * const warningGet__name__ = "warningGet";
            const char * const warningGet__doc__ = "get the state of a warning channel";
            PyObject * warningGet(PyObject *, PyObject *);

            // lookup a name in the error index
            const char * const errorLookup__name__ = "errorLookup";
            const char * const errorLookup__doc__ =
                "get the channel state from the error index";
            PyObject * errorLookup(PyObject *, PyObject *);

            // manipulate the state of a error channel
            const char * const errorSet__name__ = "errorSet";
            const char * const errorSet__doc__ = "set the state of a error channel";
            PyObject * errorSet(PyObject *, PyObject *);

            const char * const errorGet__name__ = "errorGet";
            const char * const errorGet__doc__ = "get the state of a error channel";
            PyObject * errorGet(PyObject *, PyObject *);


        } // of namespace journal
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
