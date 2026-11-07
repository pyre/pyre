// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "concepts.h"
#include "Interval.h"


// the shapes built out of other shapes
namespace pyre::geometry {
    // the smallest interval that holds both {a} and {b}
    template <line_c lineT>
    constexpr auto hull(const Interval<lineT> & a, const Interval<lineT> & b) -> Interval<lineT>;
} // namespace pyre::geometry


// get the inline definitions
#include "constructions.icc"


// end of file
