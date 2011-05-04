// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_manipulators_0_h)
#define pyre_journal_manipulators_0_h


// declaration of the injection operator with arity zero manipulators
// place this in global scope
template <typename Channel>
inline
Channel &
operator << (Channel &, Channel & (*)(Channel &));


// manipulators with zero arguments
namespace pyre {
    namespace journal {
        
        // end of insertion
        template <typename Channel>
        inline
        Channel &
        endl(Channel &);

        // new line
        template <typename Channel>
        inline
        Channel &
        newline(Channel &);
    }
}


// get the inline definitions
#define pyre_journal_manipulators_0_icc
#include "manipulators-0.icc"
#undef pyre_journal_manipulators_0_icc

#endif // pyre_journal_manipulators_0_h

// end of file
