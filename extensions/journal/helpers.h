// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// utilities
namespace pyre::journal::py {
    // build a locator that points to the nearest caller from python
    inline auto locator() -> locator_t;
} // namespace pyre::journal::py


// get the inline definitions
#include "helpers.icc"


// end of file
