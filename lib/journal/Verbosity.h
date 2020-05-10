// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved

// code guard
#if !defined(pyre_journal_Verbosity_h)
#define pyre_journal_Verbosity_h


// information about the location of the channel invocation
class pyre::journal::Verbosity
{
    // types
public:
    // the verbosity level
    using verbosity_type = size_t;

    // metamethods
public:
    // constructor
    inline explicit Verbosity(verbosity_type);

    // interface
public:
    // accessors
    inline auto verbosity() const -> verbosity_type;

    // data
private:
    const verbosity_type _verbosity;
};


// get the inline definitions
#define pyre_journal_Verbosity_icc
#include "Verbosity.icc"
#undef pyre_journal_Verbosity_icc


#endif

// end of file
