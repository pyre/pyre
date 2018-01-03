// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Error_h)
#define pyre_journal_Error_h

// place Error in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Error;
    }
}


// declaration
class pyre::journal::Error :
    public pyre::journal::Diagnostic<Error>,
    public pyre::journal::Channel<Error, true>
{
    // befriend my superclass so it can invoke my recording hooks
    friend class Diagnostic<Error>;

    // types
public:
    typedef std::string string_t;
    typedef Diagnostic<Error> diagnostic_t;
    typedef Channel<Error, true> channel_t;

    // meta methods
public:
    inline ~Error();
    inline Error(string_t name);
    // disallow
private:
    inline Error(const Error &);
    inline const Error & operator=(const Error &);
};


// get the inline definitions
#define pyre_journal_Error_icc
#include "Error.icc"
#undef pyre_journal_Error_icc


# endif
// end of file
