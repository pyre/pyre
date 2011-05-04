// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_jourmal_manipulators_h)
#define pyre_journal_manipulators_h


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
template <typename Channel, typename Manipulator>
inline
pyre::journal::Diagnostic<Channel> &
operator << (pyre::journal::Diagnostic<Channel> &, Manipulator);


// forward declarations
namespace pyre {
    namespace journal {

        // manipulators with zero arguments
        // end of insertion
        template <typename Channel>
        inline
        Channel & endl(Channel &);

        // new line
        template <typename Channel> 
        inline
        Channel & newline(Channel &);

        // manipulators with more arguments
        class at;
        class set;
    }
}

// definitions
// location
class pyre::journal::at {
    // interface
public:
    template <typename Channel>
    inline
    Diagnostic<Channel> & 
    inject(Diagnostic<Channel> & channel) const;

    // meta methods
public:
    at(const char *, int, const char * = 0);

    // data
public:
    const char * const _file;
    const int _line;
    const char * const _function;
};


// attributes
class pyre::journal::set {
    // types
public:
    typedef std::string string_t;
    // interface
public:
    template <typename Channel>
    inline
    Diagnostic<Channel> & 
    inject(Diagnostic<Channel> & channel) const;

    // meta methods
public:
    set(string_t, string_t);

    // data
public:
    const string_t _key;
    const string_t _value;
};


// get the inline definitions
#define pyre_journal_manipulators_icc
#include "manipulators.icc"
#undef pyre_journal_manipulators_icc

#endif // pyre_journal_manipulators_0_h

// end of file
