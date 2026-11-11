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
#include "Point.h"


// the affine line of time: its points are instants, stored as the seconds since its epoch, and
// two instants subtract to give a duration, a type of its own, so instants never add
class pyre::geometry::Timeline {
    // type aliases
public:
    // me
    using self_type = Timeline;
    // my coordinate: the seconds since my epoch
    using coordinate_type = double;
    // my points
    using rep_type = coordinate_type;
    using point_type = Point<self_type>;
    // the vectors between my points
    using vector_type = std::chrono::duration<double>;
    // distances, in seconds
    using distance_type = double;
    // the instants of the civil calendar
    using time_type = std::chrono::sys_time<std::chrono::duration<double>>;
    // indices
    using size_type = size_t;
    // the hashes of my points
    using hash_type = hash_t;

    // metamethods
public:
    // a timeline with the given epoch, by default the epoch of the system clock
    constexpr explicit Timeline(time_type epoch = time_type {});

    // the rest
    constexpr Timeline(const Timeline &) = default;
    constexpr Timeline(Timeline &&) = default;
    constexpr Timeline & operator=(const Timeline &) = default;
    constexpr Timeline & operator=(Timeline &&) = default;
    constexpr ~Timeline() = default;

    // equality: timelines with the same epoch are the same space
    constexpr auto operator==(const Timeline &) const -> bool = default;

    // interface
public:
    // my dimension
    static constexpr auto dimension() -> size_type;
    // my epoch
    constexpr auto epoch() const -> time_type;
    // the length of the interval between two instants
    constexpr auto distance(const point_type & p, const point_type & q) const -> distance_type;

    // the civil calendar
public:
    // the instant that falls at the given time
    constexpr auto point(time_type time) const -> point_type;
    // the time of the given instant
    constexpr auto time(const point_type & p) const -> time_type;

    // the affine structure
public:
    // the duration from {q} to {p}
    static constexpr auto difference(const rep_type & p, const rep_type & q) -> vector_type;
    // the instant {p} moved by {v}
    static constexpr auto translate(const rep_type & p, const vector_type & v) -> rep_type;
    // the opposite of {v}
    static constexpr auto opposite(const vector_type & v) -> vector_type;

    // the order of the line
public:
    // the coordinate of an instant
    static constexpr auto coordinate(const rep_type & p) -> coordinate_type;
    // the instant at the given coordinate
    static constexpr auto fromCoordinate(coordinate_type x) -> rep_type;

    // rendering
public:
    // write an instant as its seconds since the epoch
    static auto inject(std::ostream & stream, const rep_type & p) -> void;

    // hashing
public:
    // the hash of an instant, shared by the instants that compare equal
    static auto hash(const rep_type & p) -> hash_type;

    // implementation details - data
private:
    time_type _epoch;
};


// get the inline definitions
#include "Timeline.icc"


// end of file
