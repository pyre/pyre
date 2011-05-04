// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_manipulators_h)
#define pyre_journal_manipulators_h


// manipulators with one argument
namespace pyre {
    namespace journal {
        // forward declaration of arity 3 manipulators
        template <typename Channel, typename arg1_t, typename arg2_t, typename arg3_t>
        class manipulator_3;
    }
}

// the injection operator: leave this in the global namespace
template <typename Channel, typename arg1_t, typename arg2_t, typename arg3_t>
Channel &
operator<< (
            Channel &,
            pyre::journal::manipulator_3<Channel, arg1_t, arg2_t, arg3_t>
            );

// definition of one argument manipulators
template <typename Channel, typename arg1_t, typename arg2_t, typename arg3_t>
class pyre::journal::manipulator_3 {
    // declare the injection operator as a friend
    friend
    Channel &
    ::operator<< <> (Channel &, manipulator_3<Channel, arg1_t, arg2_t, arg3_t>);

    // types
public:
    typedef Channel & (*factory_t)(Channel &, arg1_t, arg2_t, arg3_t);

    // meta methods
public:
    inline manipulator_3(factory_t, arg1_t, arg2_t, arg3_t);

    // data
private:
    factory_t _factory;
    arg1_t _arg1;
    arg2_t _arg2;
    arg3_t _arg3;
};


// get the inline definitions
#define pyre_journal_manipulators_3_icc
#include "manipulators-3.icc"
#undef pyre_journal_manipulators_3_icc

#endif // pyre_journal_manipulators_h

// end of file
