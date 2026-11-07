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
#include "Collection.h"


// the symmetric relations, as the pairs of shapes that know how to compute them; each pair is
// written once, in whichever order is natural, and the relations below ask for it either way
namespace pyre::geometry::relations {
    // whether two intervals share a point
    template <line_c lineT>
    constexpr auto intersects(const Interval<lineT> & a, const Interval<lineT> & b) -> bool;

    // whether a union shares a point with a shape: one of its members does
    template <class shapeT, class otherT>
    constexpr auto intersects(const Collection<shapeT> & a, const otherT & b) -> bool;
} // namespace pyre::geometry::relations


// the relations among shapes
namespace pyre::geometry {
    // whether {a} and {b} share a point, asked of whichever of the two knows how
    template <class firstT, class secondT>
        requires(
            requires(const firstT & a, const secondT & b) {
                pyre::geometry::relations::intersects(a, b);
            }
            or requires(
                const firstT & a,
                const secondT & b) { pyre::geometry::relations::intersects(b, a); })
    constexpr auto intersects(const firstT & a, const secondT & b) -> bool;

    // whether every point of {b} is a point of {a}; this one isn't symmetric, so each order
    // is a relation of its own
    // between two intervals
    template <line_c lineT>
    constexpr auto covers(const Interval<lineT> & a, const Interval<lineT> & b) -> bool;
    // between a union of intervals and an interval, which its members may cover together
    template <line_c lineT>
    constexpr auto covers(const Collection<Interval<lineT>> & a, const Interval<lineT> & b) -> bool;
    // between a shape and a union, which the shape covers when it covers every member
    template <class shapeT, class memberT>
    constexpr auto covers(const shapeT & a, const Collection<memberT> & b) -> bool;
} // namespace pyre::geometry


// get the inline definitions
#include "relations.icc"


// end of file
