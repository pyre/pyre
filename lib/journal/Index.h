// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Index_h)
#define pyre_journal_Index_h

// place Index in namespace pyre::journal
namespace pyre {
    namespace journal {
        template <typename> class Index;
    }
}

// This class maintains the map
//
//    (severity, channel) -> value
//
// to enable the maintenance of per-channel information. For example, {Chronicler} owns an
// {Index<bool>} to hold the activation state of output channels.

// declaration
template <typename Value>
class pyre::journal::Index {

    // types
public:
    typedef Value value_t;
    typedef std::string string_t;
    typedef std::pair<string_t, string_t> key_t;
    typedef std::map<key_t, value_t> index_t;

    // interface: place the public methods here
public:
    inline value_t & lookup(const string_t & severity, const string_t & channel);

    // meta methods: constructors, destructors
public:
    inline ~Index();
    inline Index();
    // disable
private:
    inline Index(const Index &);
    inline const Index & operator=(const Index &);
    
    // data members
private:
    index_t _index;
};


// get the inline definitions
#define pyre_journal_Index_icc
#include "Index.icc"
#undef pyre_journal_Index_icc


# endif
// end of file
