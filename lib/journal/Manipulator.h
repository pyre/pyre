// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_manipulator_h)
#define pyre_journal_manipulator_h


// forward declarations
namespace pyre {
    namespace journal {
        template <typename Injector> class Manipulator;
    }
}

// the base manipulator; necessary as a marker to disambiguate our overloaded {operator <<}
template <typename Injector>
class pyre::journal::Manipulator {
    // interface
public:
    template <typename Channel>
    Diagnostic<Channel> &
    inject(Diagnostic<Channel> &) const;

    // meta methods
public:
    inline ~Manipulator();
    inline Manipulator();
    inline Manipulator(const Manipulator &);
    inline Manipulator & operator= (const Manipulator &);
};


// get the inline definitions
#define pyre_journal_Manipulator_icc
#include "Manipulator.icc"
#undef pyre_journal_Manipulator_icc

#endif // pyre_journal_manipulators_0_h

// end of file
