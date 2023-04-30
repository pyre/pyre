// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Locator_h)
#define pyre_journal_Locator_h


// information about the location of the channel invocation
class pyre::journal::Locator
{
    // types
public:
    // the data held by {Locator} are used to create message notes
    using value_type = value_t;

    // metamethods
public:
    // constructor
    // modern version; preferred when instantiating explicitly
    inline Locator(const value_type &, const value_type &, const value_type &);
    // legacy version; used by the {__HERE__} locator factories
    inline explicit Locator(const char * = "", int = 0, const char * = "");

    // interface
public:
    // accessors
    inline auto file() const -> const value_type &;
    inline auto line() const -> const value_type &;
    inline auto func() const -> const value_type &;

    // data
private:
    const value_type _file;
    const value_type _line;
    const value_type _func;
};


// get the inline definitions
#define pyre_journal_Locator_icc
#include "Locator.icc"
#undef pyre_journal_Locator_icc


#endif

// end of file
