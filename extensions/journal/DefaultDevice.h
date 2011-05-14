// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_extensions_journal_DefaultDevice_h)
#define pyre_extensions_journal_DefaultDevice_h

// place DefaultDevice in namespace pyre::journal
namespace pyre {
    namespace extensions {
        namespace journal {
            class DefaultDevice;
        }
    }
}

// declaration
class pyre::extensions::journal::DefaultDevice : public pyre::journal::Device {
    // interface
public:
    virtual void record(entry_t &, metadata_t &);

    // meta methods
public:
    virtual ~DefaultDevice();
    inline DefaultDevice(PyObject * owner);
    // disallow
private:
    DefaultDevice(const DefaultDevice &);
    const DefaultDevice & operator=(const DefaultDevice &);

    // data
private:
    PyObject * _owner;
};


// get the inline definitions
#define pyre_extensions_journal_DefaultDevice_icc
#include "DefaultDevice.icc"
#undef pyre_extensions_journal_DefaultDevice_icc

# endif

// end of file
