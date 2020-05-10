// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved

// code guard
#if !defined(pyre_journal_exceptions_h)
#define pyre_journal_exceptions_h


// exception raised by errors
class pyre::journal::application_error : public std::runtime_error {
    // types
public:
    using string_type = string_t;

    // metamethods
public:
    inline application_error(const char *);
    inline application_error(const string_type &);
};


// exception raised by firewalls
class pyre::journal::firewall_error : public std::logic_error {
    // types
public:
    using string_type = string_t;

    // metamethods
public:
    inline firewall_error(const char *);
    inline firewall_error(const string_type &);
};


// exception raised by debug channels when marked fatal
class pyre::journal::debug_error : public std::logic_error {
    // types
public:
    using string_type = string_t;

    // metamethods
public:
    inline debug_error(const char *);
    inline debug_error(const string_type &);
};


// get the inline definitions
#define pyre_journal_exceptions_icc
#include "exceptions.icc"
#undef pyre_journal_exceptions_icc


#endif

// end of file
