// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_State_h)
#define pyre_journal_State_h

// place State in namespace pyre::journal
namespace pyre {
    namespace journal {
        template <bool = true> class State;
        class Device;
    }
}


// declaration
template <bool Default>
class pyre::journal::State {
    // types
public:
    typedef bool state_t;
    typedef Device device_t;

    // interface
public:
    // accessors
    inline state_t state() const;
    inline const device_t & device() const;

    // mutators
    inline void activate();
    inline void deactivate();
    inline void device(device_t *);

    // meta methods
public:
    inline ~State();
    inline State(state_t = Default, device_t * = 0);
    inline State(const State &);
    inline const State & operator=(const State &);
    
    // data members
private:
    state_t _state;
    device_t * _device;
};


// get the inline definitions
#define pyre_journal_State_icc
#include "State.icc"
#undef pyre_journal_State_icc


# endif
// end of file
