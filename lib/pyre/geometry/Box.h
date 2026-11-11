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
#include "spherical.h"


// a box in the longitude-latitude chart: the points whose longitude lies between two meridians
// and whose latitude lies between two parallels, all in degrees; the longitudes run east from
// the {west} meridian to the {east} one, so a box whose west edge is east of its east edge
// straddles the antimeridian, and a box from -180 to 180 holds every longitude; its edges along
// the parallels are straight in the chart and are not great circles; the box whose south edge is
// north of its north edge holds nothing, and all such boxes are the same empty one
template <class chartT>
class pyre::geometry::Box {
    // type aliases
public:
    // me
    using self_type = Box<chartT>;
    // my chart
    using chart_type = chartT;
    // its space
    using space_type = typename chart_type::space_type;
    // and its points
    using point_type = Point<space_type>;
    // the boxes are their own envelopes
    using envelope_type = self_type;
    // the polygon with my points
    using polygon_type = Polygon<chart_type>;
    // the points of the space around the sphere
    using vector_type = spherical::vector_t;
    // my hash
    using hash_type = hash_t;

    // constants
public:
    // the degrees by which a point may miss an edge and still be on it, and two boxes may miss
    // each other and still touch: the coordinates of a point come back from its unit vector with
    // a rounding error of about 1e-14 degrees, so a point placed exactly on an edge would
    // otherwise land on either side of it; a nanodegree is about a tenth of a millimeter on the
    // ground
    static constexpr auto slack = 1e-9;

    // metamethods
public:
    // the empty box
    constexpr Box();
    // the box between the given meridians and parallels
    constexpr Box(double west, double south, double east, double north);

    // the rest
    constexpr Box(const Box &) = default;
    constexpr Box(Box &&) = default;
    constexpr Box & operator=(const Box &) = default;
    constexpr Box & operator=(Box &&) = default;
    constexpr ~Box() = default;

    // equality
    constexpr auto operator==(const Box &) const -> bool = default;

    // factories
public:
    // the whole sphere
    static constexpr auto sphere() -> self_type;
    // the smallest box that holds the given points, in order, joined by great-circle arcs
    static auto around(const std::vector<vector_type> & points) -> self_type;

    // interface
public:
    // my edges
    constexpr auto west() const -> double;
    constexpr auto south() const -> double;
    constexpr auto east() const -> double;
    constexpr auto north() const -> double;
    // the degrees of longitude from my west edge to my east edge
    constexpr auto width() const -> double;
    // whether i hold no points
    constexpr auto empty() const -> bool;
    // whether i hold every longitude
    constexpr auto full() const -> bool;
    // whether i hold the point {p}
    auto contains(const point_type & p) const -> bool;
    // whether the longitude {longitude}, in degrees, is between my meridians
    constexpr auto spans(double longitude) const -> bool;
    // the smallest box that holds me
    constexpr auto envelope() const -> envelope_type;
    // the polygon with my points, for the relations with shapes that are not boxes; the box must
    // not be empty, since no polygon holds nothing
    auto polygon() const -> polygon_type;

    // hashing
public:
    // my hash, shared by the boxes that compare equal
    auto hash() const -> hash_type;

    // implementation details
private:
    // the points along the parallel at {latitude}, from {from} for {degrees} of longitude, east
    // when {degrees} is positive and west when it is negative
    static auto parallel(double latitude, double from, double degrees)
        -> std::vector<std::array<double, 2>>;
    // the points along the meridian at {longitude}, from the latitude {from} to the latitude {to}
    static auto meridian(double longitude, double from, double to)
        -> std::vector<std::array<double, 2>>;

    // implementation details - data
private:
    double _west;
    double _south;
    double _east;
    double _north;
};


// get the inline definitions
#include "Box.icc"


// end of file
