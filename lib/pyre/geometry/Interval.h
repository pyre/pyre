// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "hashing.h"
#include "concepts.h"
#include "Point.h"


// a closed interval of a line: the points between its two ends, the ends included; an end at an
// infinity leaves the interval unbounded on that side, and an interval whose lower end lies
// above its upper one holds no points at all, so all such intervals are the same empty one
template <class lineT>
class pyre::geometry::Interval {
    // the intervals live on lines
    static_assert(line_c<lineT>, "intervals live on lines");

    // type aliases
public:
    // me
    using self_type = Interval<lineT>;
    // my line
    using line_type = lineT;
    // its points
    using point_type = Point<line_type>;
    // and its coordinate
    using coordinate_type = typename line_type::coordinate_type;
    // the smallest interval that holds me is me
    using envelope_type = self_type;
    // my hash
    using hash_type = hash_t;

    // metamethods
public:
    // the empty interval
    constexpr Interval();
    // the interval between {lower} and {upper}
    constexpr Interval(const point_type & lower, const point_type & upper);

    // the rest
    constexpr Interval(const Interval &) = default;
    constexpr Interval(Interval &&) = default;
    constexpr Interval & operator=(const Interval &) = default;
    constexpr Interval & operator=(Interval &&) = default;
    constexpr ~Interval() = default;

    // equality
    constexpr auto operator==(const Interval &) const -> bool = default;

    // the unbounded intervals
public:
    // the whole line
    static constexpr auto line() -> self_type;
    // the points at or above {lower}
    static constexpr auto from(const point_type & lower) -> self_type;
    // the points at or below {upper}
    static constexpr auto until(const point_type & upper) -> self_type;

    // interface
public:
    // my ends
    constexpr auto lower() const -> point_type;
    constexpr auto upper() const -> point_type;
    // whether i hold no points
    constexpr auto empty() const -> bool;
    // whether i have a lower end on the line
    constexpr auto boundedBelow() const -> bool;
    // whether i have an upper end on the line
    constexpr auto boundedAbove() const -> bool;
    // whether i hold the point {p}
    constexpr auto contains(const point_type & p) const -> bool;
    // the smallest interval that holds me
    constexpr auto envelope() const -> envelope_type;

    // hashing
public:
    // my hash, shared by the intervals that compare equal
    auto hash() const -> hash_type;

    // implementation details
private:
    // the coordinates of the ends of the line
    static constexpr auto lowest() -> coordinate_type;
    static constexpr auto highest() -> coordinate_type;

    // implementation details - data
private:
    point_type _lower;
    point_type _upper;
};


// get the inline definitions
#include "Interval.icc"


// end of file
