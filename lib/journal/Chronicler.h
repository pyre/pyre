// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Chronicler_h)
#define pyre_journal_Chronicler_h

// place Chronicler in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Chronicler;
    }
}

// This class is the main resting place for the various journal parts
//
// It maintains an index with the activation state of journal channels. This index is primed at
// construction time with settings from the environment variable {DEBUG_OPT}. Diagnostics
// access the index at construction time to discover whether they are enabled, and therefore
// allowed to generate output

// declaration
class pyre::journal::Chronicler {
    // types
public:
    typedef Index<bool> index_t;
    typedef typename index_t::value_t state_t;
    typedef typename index_t::string_t string_t;

    // interface
public:
    inline state_t & getChannelState(const string_t & severity, const string_t & channel);

    // meta methods
public:
    inline ~Chronicler();
    inline Chronicler();
    // disallow
private:
    inline Chronicler(const Chronicler &);
    inline const Chronicler & operator=(const Chronicler &);
    
    // data members
private:
    index_t _channels;
};


// get the inline definitions
#define pyre_journal_Chronicler_icc
#include "Chronicler.icc"
#undef pyre_journal_Chronicler_icc


# endif
// end of file
