// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Channel)
#define pyre_journal_Channel

// place Inventory in namespace pyre::journal
namespace pyre {
    namespace journal {
        template <typename, bool> class Channel;
    }
}


// declaration
template <typename Severity, bool DefaultState=true>
class pyre::journal::Channel {
    // types
public:
    typedef std::string string_t;
    typedef Inventory<DefaultState> inventory_t;
    typedef typename inventory_t::state_t state_t;
    typedef typename inventory_t::device_t device_t;
    typedef Index<inventory_t> index_t;

    // interface
public:
    // accessors
    inline state_t isActive() const;
    inline device_t * device() const;

    // mutators
    inline void activate();
    inline void deactivate();
    inline void device(device_t *);

    // access to the index
    inline static inventory_t & lookup(string_t name);

    // meta methods
public:
    inline operator bool() const;

protected:
    inline ~Channel();
    inline Channel(string_t);

    // disallow
private:
    inline Channel(const Channel &);
    inline const Channel & operator=(const Channel &);

    // data members
private:
    string_t _name;
    inventory_t & _inventory;
    // per class
    static index_t _index;
};


// get the inline definitions
#define pyre_journal_Channel_icc
#include "Channel.icc"
#undef pyre_journal_Channel_icc


# endif
// end of file
