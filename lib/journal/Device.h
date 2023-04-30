// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Device_h)
#define pyre_journal_Device_h


// the base class of all journal devices
class pyre::journal::Device {
    // types
public:
    // pointers to me
    using pointer_type = device_ptr;
    // for naming device instances
    using name_type = name_t;
    // message entry
    using entry_type = entry_t;

    // metamethods
public:
    // constructor
    inline explicit Device(const name_type &);
    // destructor
    virtual ~Device();

    // interface
public:
    // accessor
    inline auto name() const -> const name_type &;

    // abstract
    virtual auto alert(const entry_type &) -> Device & = 0;
    virtual auto help(const entry_type &) -> Device & = 0;
    virtual auto memo(const entry_type &) -> Device & = 0;

    // data
private:
    name_type _name;

    // disallow
private:
    Device(const Device &) = delete;
    Device(const Device &&) = delete;
    const Device & operator=(const Device &) = delete;
    const Device & operator=(const Device &&) = delete;
};


// get the inline definitions
#define pyre_journal_Device_icc
#include "Device.icc"
#undef pyre_journal_Device_icc


#endif

// end of file
