// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_exceptions_h)
#define pyre_journal_exceptions_h


// exception raised by errors
class pyre::journal::application_error : public std::runtime_error {
    // types
public:
    using headline_type = string_t;
    using page_type = page_t;
    using notes_type = notes_t;
    using page_const_reference = const page_t &;
    using notes_const_reference = const notes_t &;

    // metamethods
public:
    inline application_error(const headline_type &, const page_type &, const notes_type &);

    // accessors
public:
    inline auto page() const -> page_const_reference;
    inline auto notes() const -> notes_const_reference;

    // implementation details: extra data
private:
    page_type _page;
    notes_type _notes;
};


// exception raised by firewalls
class pyre::journal::firewall_error : public std::logic_error {
    // types
public:
    using headline_type = string_t;
    using page_type = page_t;
    using notes_type = notes_t;
    using page_const_reference = const page_t &;
    using notes_const_reference = const notes_t &;

    // metamethods
public:
    inline firewall_error(const headline_type &, const page_type &, const notes_type &);

    // accessors
public:
    inline auto page() const -> page_const_reference;
    inline auto notes() const -> notes_const_reference;

    // implementation details: extra data
private:
    page_type _page;
    notes_type _notes;
};


// exception raised by debug channels when marked fatal
class pyre::journal::debug_error : public std::logic_error {
    // types
public:
    using headline_type = string_t;
    using page_type = page_t;
    using notes_type = notes_t;
    using page_const_reference = const page_t &;
    using notes_const_reference = const notes_t &;

    // metamethods
public:
    inline debug_error(const headline_type &, const page_type &, const notes_type &);

    // accessors
public:
    inline auto page() const -> page_const_reference;
    inline auto notes() const -> notes_const_reference;

    // implementation details: extra data
private:
    page_type _page;
    notes_type _notes;
};


// get the inline definitions
#define pyre_journal_exceptions_icc
#include "exceptions.icc"
#undef pyre_journal_exceptions_icc


#endif

// end of file
