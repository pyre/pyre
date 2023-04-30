// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Flush_h)
#define pyre_journal_Flush_h


// flush a channel after injecting a decorator
template <typename decoratorT>
class pyre::journal::Flush
{
public:
    using decorator_type = decoratorT;

    // metamethods
public:
    // constructor
    inline Flush(decorator_type decorator);

    // interface
public:
    inline auto decorator() const -> const decorator_type &;

    // data
private:
    decorator_type _decorator;
};


// get the inline definitions
#define pyre_journal_Flush_icc
#include "Flush.icc"
#undef pyre_journal_Flush_icc


#endif

// end of file
