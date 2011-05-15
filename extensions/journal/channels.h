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
            const char * const lookupDebug__name__ = "lookupDebugInventory";
            const char * const lookupDebug__doc__ = "get the channel state from the debug index";
            PyObject * lookupDebug(PyObject *, PyObject *);
            // lookup a name in the firewall index
            const char * const lookupFirewall__name__ = "lookupFirewallInventory";
            const char * const lookupFirewall__doc__ = 
                "get the channel state from the firewall index";
            PyObject * lookupFirewall(PyObject *, PyObject *);
            // lookup a name in the info index
            const char * const lookupInfo__name__ = "lookupInfoInventory";
            const char * const lookupInfo__doc__ = "get the channel state from the info index";
            PyObject * lookupInfo(PyObject *, PyObject *);
            // lookup a name in the warning index
            const char * const lookupWarning__name__ = "lookupWarningInventory";
            const char * const lookupWarning__doc__ =
                "get the channel state from the warning index";
            PyObject * lookupWarning(PyObject *, PyObject *);
            // lookup a name in the error index
            const char * const lookupError__name__ = "lookupErrorInventory";
            const char * const lookupError__doc__ =
                "get the channel state from the error index";
            PyObject * lookupError(PyObject *, PyObject *);

            // access the state of Inventory<true>
            const char * const setEnabledState__name__ = "setEnabledState";
            const char * const setEnabledState__doc__ = "set the state of a normally on channel";
            PyObject * setEnabledState(PyObject *, PyObject *);

            const char * const getEnabledState__name__ = "getEnabledState";
            const char * const getEnabledState__doc__ = "get the state of a normally on channel";
            PyObject * getEnabledState(PyObject *, PyObject *);

            // access the state of Inventory<false>
            const char * const setDisabledState__name__ = "setDisabledState";
            const char * const setDisabledState__doc__ = "set the state of a normally off channel";
            PyObject * setDisabledState(PyObject *, PyObject *);

            const char * const getDisabledState__name__ = "getDisabledState";
            const char * const getDisabledState__doc__ = "get the state of a normally off channel";
            PyObject * getDisabledState(PyObject *, PyObject *);

        } // of namespace journal
    } // of namespace extensions
} // of namespace pyre

#endif

// end of file
