// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_manipulators_h)
#define pyre_journal_manipulators_h


// manipulators with zero arguments
namespace pyre {
    namespace journal {
        
        // definition of the injection operator with arity zero manipulators
        template <typename Diagnostic>
        inline
        Diagnostic &
        operator << (
                     Diagnostic & diagnostic,
                     Diagnostic & (*manipulator)(Diagnostic &)
                     ) {
            return manipulator(diagnostic);
        }

        // end of insertion
        template <typename Diagnostic>
        inline
        Diagnostic &
        endl(Diagnostic & diagnostic) {
            std::cout << "    endl" << std::endl;
            return diagnostic;
        }
    }
}


// manipulators with one, two and three arguments
namespace pyre {
    namespace journal {

        template <typename Severity, typename arg1_t> class manipulator_1;
        template <typename Severity, typename arg1_t, typename arg2_t> class manipulator_2;
        template <typename Severity, typename arg1_t, typename arg2_t, typename arg3_t> 
            class manipulator_3;

    }
}

// the injection operators: leave these in the global namespace
// injection of manipulators with one argument
template <typename Severity, typename arg1_t>
pyre::journal::Diagnostic<Severity> &
operator<< (
            pyre::journal::Diagnostic<Severity> &,
            pyre::journal::manipulator_1<Severity, arg1_t>
            );

// definition of one argument manipulators
template <typename Severity, typename arg1_t>
class pyre::journal::manipulator_1 {
    // types
public:
    typedef Diagnostic<Severity> diagnostic_t;

    // declare the injection operator as a friend
    friend
    diagnostic_t &
    ::operator<< <> (diagnostic_t &, manipulator_1<Severity, arg1_t>);

};

#endif // pyre_journal_manipulators_h

// end of file
