// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Diagnostic_h)
#define pyre_journal_Diagnostic_h

// place Diagnostic in namespace pyre::journal
namespace pyre {
    namespace journal {
        template <typename> class Diagnostic;
    }
}

// imported types and other includes


// declaration
template <typename Severity>
class pyre::journal::Diagnostic {
    // types: place typedefs here
public:
    typedef int member_t;
    typedef Severity severity_t;

    // interface
public:
    Diagnostic & record();
    Diagnostic & newline();

    // meta methods
public:
    inline ~Diagnostic();
    inline Diagnostic();
    inline Diagnostic(const Diagnostic &);
    inline Diagnostic & operator=(const Diagnostic &);
    
    // data members
private:
};


// get the inline definitions
#define pyre_journal_Diagnostic_icc
#include "Diagnostic.icc"
#undef pyre_journal_Diagnostic_icc


# endif
// end of file
