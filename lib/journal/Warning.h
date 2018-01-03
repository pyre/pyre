// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Warning_h)
#define pyre_journal_Warning_h

// place Warning in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Warning;
    }
}


// declaration
class pyre::journal::Warning :
    public pyre::journal::Diagnostic<Warning>,
    public pyre::journal::Channel<Warning, true>
{
    // befriend my superclass so it can invoke my recording hooks
    friend class Diagnostic<Warning>;

    // types
public:
    typedef std::string string_t;
    typedef Diagnostic<Warning> diagnostic_t;
    typedef Channel<Warning, true> channel_t;

    // meta methods
public:
    inline ~Warning();
    inline Warning(string_t name);
    // disallow
private:
    inline Warning(const Warning &);
    inline const Warning & operator=(const Warning &);
};


// get the inline definitions
#define pyre_journal_Warning_icc
#include "Warning.icc"
#undef pyre_journal_Warning_icc


# endif
// end of file
