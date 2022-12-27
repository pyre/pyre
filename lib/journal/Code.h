// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Code_h)
#define pyre_journal_Code_h


// attach a code to a message
class pyre::journal::Code {
    // types
public:
    // codes are strings
    using code_type = string_t;

    // metamethods
public:
    // constructor
    inline explicit Code(code_type);

    // interface
public:
    // accessors
    inline auto code() const -> code_type;

    // data
private:
    const code_type _code;
};


// get the inline definitions
#define pyre_journal_Code_icc
#include "Code.icc"
#undef pyre_journal_Code_icc


#endif

// end of file
