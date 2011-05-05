// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_manipulators_h)
#define pyre_journal_manipulators_h


// forward declarations
namespace pyre {
    namespace journal {

        // manipulators with zero arguments
        // end of insertion
        template <typename Channel> inline Channel & endl(Channel &);
        // new line
        template <typename Channel> inline Channel & newline(Channel &);
    }
}

// declaration of the injection operators; place these in global scope
// injection by function
template <typename Channel>
inline
pyre::journal::Diagnostic<Channel> &
operator << (
             pyre::journal::Diagnostic<Channel> &,
             pyre::journal::Diagnostic<Channel> &
             (*)(pyre::journal::Diagnostic<Channel> &));

// injection by manipulator
template <typename Channel>
inline
pyre::journal::Diagnostic<Channel> &
operator << (pyre::journal::Diagnostic<Channel> &, const pyre::journal::Locator &);

template <typename Channel>
inline
pyre::journal::Diagnostic<Channel> &
operator << (pyre::journal::Diagnostic<Channel> &, const pyre::journal::Selector &);


// get the inline definitions
#define pyre_journal_manipulators_icc
#include "manipulators.icc"
#undef pyre_journal_manipulators_icc

#endif // pyre_journal_manipulators_0_h

// end of file
