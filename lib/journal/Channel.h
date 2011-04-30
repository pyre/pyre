// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Channel_h)
#define pyre_journal_Channel_h

// place Channel in namespace pyre::journal
namespace pyre {
     namespace journal {
         template <bool> class Channel;
         template <typename> class Index;
     }
}


// declaration
template <bool DefaultState>
class pyre::journal::Channel {
    // types: place typedefs here
public:
    typedef std::string string_t;
    typedef State<DefaultState> state_t;
    typedef Index<state_t> index_t;

    // interface: place the public methods here
public:

    // meta methods: constructors, destructors
public:
    inline ~Channel();
    inline Channel(string_t);
    inline Channel(const Channel &);
    inline const Channel & operator=(const Channel &);
    
    // data members
private:
    // per-instance
    string_t _name;

    // per-class
    static index_t _index;
};


// get the inline definitions
#define pyre_journal_Channel_icc
#include "Channel.icc"
#undef pyre_journal_Channel_icc


# endif
// end of file
