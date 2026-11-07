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
#include "Box.h"
#include "Ring.h"
#include "Polygon.h"


// the shapes built out of other shapes
namespace pyre::geometry {
    // the smallest interval that holds both {a} and {b}
    template <line_c lineT>
    constexpr auto hull(const Interval<lineT> & a, const Interval<lineT> & b) -> Interval<lineT>;
    // the smallest box that holds both {a} and {b}, the shorter way around in longitude
    template <class chartT>
    auto hull(const Box<chartT> & a, const Box<chartT> & b) -> Box<chartT>;

    // the {ring}, walked in the direction that makes it bound the smaller of its two regions
    //
    // a ring bounds the region to its left, the only rule that can describe every region on the
    // sphere, and an unforgiving one: a ring walked the wrong way describes the complement of
    // what was meant; rings drawn or typed by people come in either direction, and everything
    // they draw on a map is smaller than a hemisphere, so this is the right reading of their
    // rings; it is the wrong one for data whose convention is known, which is read with it, and
    // for regions larger than a hemisphere, which it silently flips; see the section on regions
    // on the sphere in doc/design/geometry.md
    template <class chartT>
    auto orient(const Ring<chartT> & ring) -> Ring<chartT>;
    // the {polygon}, with its first ring around the smaller of its two regions and the others,
    // its holes, around the larger, so that the region to the left of each hole is everything
    // outside of it
    template <class chartT>
    auto orient(const Polygon<chartT> & polygon) -> Polygon<chartT>;
} // namespace pyre::geometry


// get the inline definitions
#include "constructions.icc"


// end of file
