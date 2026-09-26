// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// my dependencies
#include "forward.h"


// loose functions shared by the visualization workflows
namespace pyre::viz {
    // the magnitude of a cell of any of the supported types: its absolute value, its modulus
    // when it is complex, and the cell itself when it is unsigned, which has no absolute value
    // of its own to ask for
    template <typename valueT>
    inline auto magnitude(const valueT & value) -> double;
} // namespace pyre::viz


// the inline definitions
#include "utilities.icc"


// end of file
