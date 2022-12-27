// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Dent_h)
#define pyre_journal_Dent_h


// information about the location of the channel invocation
class pyre::journal::Dent {
    // types
public:
    // {Dent} remembers a {dent_t} level
    using dent_type = dent_t;

    // metamethods
public:
    // constructor
    inline explicit Dent(dent_type);

    // interface
public:
    // accessors
    inline auto dent() const -> dent_type;

    // data
private:
    const dent_type _dent;
};


// get the inline definitions
#define pyre_journal_Dent_icc
#include "Dent.icc"
#undef pyre_journal_Dent_icc


#endif

// end of file
