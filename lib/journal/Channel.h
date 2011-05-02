// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Channel)
#define pyre_journal_Channel

// place Inventory in namespace pyre::journal
namespace pyre {
    namespace journal {
        template <bool> class Channel;
    }
}


// declaration
template <bool DefaultState>
class pyre::journal::Channel {
    // types
public:
    typedef Inventory<DefaultState> inventory_t;
    typedef typename inventory_t::state_t state_t;
    typedef typename inventory_t::device_t device_t;

    // interface
public:
    // accessors
    inline state_t isActive() const;
    inline const device_t & device() const;

    // mutators
    inline void activate();
    inline void deactivate();
    inline void device(device_t *);

    // meta methods
public:
    inline ~Channel();
    inline Channel(inventory_t &);
    inline Channel(const Channel &);
    inline const Channel & operator=(const Channel &);
    
    // data members
private:
    inventory_t & _inventory;
};


// get the inline definitions
#define pyre_journal_Channel_icc
#include "Channel.icc"
#undef pyre_journal_Channel_icc


# endif
// end of file
