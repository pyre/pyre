// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Note_h)
#define pyre_journal_Note_h


// notes are channel manipulators that decorate channels with metadata
class pyre::journal::Note
{
    // types
public:
    using key_type = key_t;
    using value_type = value_t;

    // metamethods
public:
    // constructor
    inline Note(key_type, value_type);

    // interface
public:
    inline auto key() const -> const key_type &;
    inline auto value() const -> const value_type &;

    // data
private:
    key_type _key;
    value_type _value;
};


// get the inline definitions
#define pyre_journal_Note_icc
#include "Note.icc"
#undef pyre_journal_Note_icc


#endif

// end of file
