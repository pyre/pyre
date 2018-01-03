// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
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


// declaration
class pyre::journal::Debug :
    public pyre::journal::Diagnostic<Debug>,
    public pyre::journal::Channel<Debug, false>
{
    // types
public:
    typedef std::string string_t;
    typedef Diagnostic<Debug> diagnostic_t;
    typedef Channel<Debug, false> channel_t;

    // meta methods
public:
    inline ~Debug();
    inline Debug(string_t name);
    // disallow
private:
    inline Debug(const Debug &);
    inline const Debug & operator=(const Debug &);
};


// get the inline definitions
#define pyre_journal_Debug_icc
#include "Debug.icc"
#undef pyre_journal_Debug_icc


# endif
// end of file
