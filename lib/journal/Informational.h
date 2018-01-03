// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Informational_h)
#define pyre_journal_Informational_h

// place Informational in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Informational;
    }
}


// declaration
class pyre::journal::Informational :
    public pyre::journal::Diagnostic<Informational>,
    public pyre::journal::Channel<Informational, true>
{
    // types
public:
    typedef std::string string_t;
    typedef Diagnostic<Informational> diagnostic_t;
    typedef Channel<Informational, true> channel_t;

    // meta methods
public:
    inline ~Informational();
    inline Informational(string_t name);
    // disallow
private:
    inline Informational(const Informational &);
    inline const Informational & operator=(const Informational &);
};


// get the inline definitions
#define pyre_journal_Informational_icc
#include "Informational.icc"
#undef pyre_journal_Informational_icc


# endif
// end of file
