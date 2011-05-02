// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Debug_h)
#define pyre_journal_Debug_h

// place Debug in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Debug;
    }
}

// imported types and other includes


// declaration
class pyre::journal::Debug {
    // types
public:
    typedef std::string string_t;
    typedef Inventory<false> inventory_t;
    typedef Index<inventory_t> index_t;

    // interface
public:

    // meta methods
public:
    inline ~Debug();
    inline Debug(string_t name);
    inline Debug(const Debug &);
    inline const Debug & operator=(const Debug &);
    
    // data members
private:
    string_t _name;

    // per-class
    static index_t _index;
};


// get the inline definitions
#define pyre_journal_Debug_icc
#include "Debug.icc"
#undef pyre_journal_Debug_icc


# endif
// end of file
