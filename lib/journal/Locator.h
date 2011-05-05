// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_Locator_h)
#define pyre_journal_Locator_h


// forward declarations
namespace pyre {
    namespace journal {
        class Locator;
    }
}


// overload the injection operators; should be at global scope
template <typename Channel>
inline
pyre::journal::Diagnostic<Channel> &
operator << (pyre::journal::Diagnostic<Channel> &, const pyre::journal::Locator &);


// locator
class pyre::journal::Locator {
    // interface
public:
    template <typename Channel>
    inline
    Diagnostic<Channel> & 
    inject(Diagnostic<Channel> & channel) const;

    // meta methods
public:
    inline ~Locator();
    inline Locator(const char *, int, const char * = 0);
private:
    inline Locator(const Locator &);
    inline Locator & operator=(const Locator &);

    // data
private:
    const char * _file;
    int _line;
    const char * _function;
};


// get the inline definitions
#define pyre_journal_Locator_icc
#include "Locator.icc"
#undef pyre_journal_Locator_icc

#endif // pyre_journal_manipulators_0_h

// end of file
