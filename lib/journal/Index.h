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
        class Index;
    }
}


// declaration
class pyre::journal::Index {

    // types
public:
    typedef bool state_t;
    typedef std::string string_t;
    typedef std::pair<string_t, string_t> key_t;
    typedef std::map<key_t, state_t> index_t;

    // interface: place the public methods here
public:
    inline state_t & lookup(const string_t & channel, const string_t & name);

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
