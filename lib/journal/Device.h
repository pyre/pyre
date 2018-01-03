// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Device_h)
#define pyre_journal_Device_h

// place Device in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Device;
    }
}

// declaration
class pyre::journal::Device {
    // types
public:
    typedef std::string string_t;
    typedef std::vector<string_t> entry_t;
    typedef std::map<string_t, string_t> metadata_t;

    // interface
public:
    virtual void record(entry_t &, metadata_t &) = 0;

    // meta methods
public:
    virtual ~Device();
    inline Device();
    // disallow
private:
    Device(const Device &);
    const Device & operator=(const Device &);
};


// get the inline definitions
#define pyre_journal_Device_icc
#include "Device.icc"
#undef pyre_journal_Device_icc


# endif
// end of file
