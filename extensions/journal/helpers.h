// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_py_helpers_h)
#define pyre_journal_py_helpers_h


// utilities
namespace pyre::journal::py {
    // build a locator that points to the nearest caller from python
    inline auto locator() -> locator_t;
}


// get the inline definitions
#define pyre_journal_py_helpers_icc
#include "helpers.icc"
#undef pyre_journal_py_helpers_icc


#endif

// end of file
