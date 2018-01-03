// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//


#if !defined(pyre_journal_manipulators_h)
#define pyre_journal_manipulators_h


// forward declarations
namespace pyre {
    namespace journal {

        // manipulators with zero arguments
        // end of insertion
        inline Null & endl(Null &);
        template <typename Channel> inline Channel & endl(Channel &);
        // new line
        inline Null & newline(Null &);
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


// injection on null diagnostics
inline
pyre::journal::Null &
operator << (
             pyre::journal::Null &,
             pyre::journal::Null & (*)(pyre::journal::Null &));


#define pyre_journal_manipulators_icc
#include "manipulators.icc"
#undef pyre_journal_manipulators_icc

#endif // pyre_journal_manipulators_0_h

// end of file
