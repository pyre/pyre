// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "Point.h"
#include "Ring.h"
#include "Box.h"


// a polygon on the sphere: the points in the regions bound by all of its rings, each of which
// bounds the region to its left; the first ring runs counterclockwise around the polygon and the
// others clockwise around its holes, so that the region to the left of each hole is everything
// outside of it; a polygon without rings is the whole sphere; see {Ring} for why a ring bounds
// the region to its left, and {orient} for rings whose direction is not known
template <class chartT>
class pyre::geometry::Polygon {
    // type aliases
public:
    // me
    using self_type = Polygon<chartT>;
    // my chart
    using chart_type = chartT;
    // its space
    using space_type = typename chart_type::space_type;
    // and its points
    using point_type = Point<space_type>;
    // my rings
    using ring_type = Ring<chart_type>;
    using rings_type = std::vector<ring_type>;
    // the smallest shape of the chart that holds me
    using envelope_type = Box<chart_type>;

    // metamethods
public:
    // the region bound by all of the {rings}
    explicit Polygon(const rings_type & rings);

    // the rest
    Polygon(const Polygon &) = default;
    Polygon(Polygon &&) = default;
    Polygon & operator=(const Polygon &) = default;
    Polygon & operator=(Polygon &&) = default;
    ~Polygon() = default;

    // equality: polygons with the same rings
    auto operator==(const Polygon &) const -> bool = default;

    // interface
public:
    // my rings
    auto rings() const -> const rings_type &;
    // whether the point {p} is in me, boundary included
    auto contains(const point_type & p) const -> bool;
    // the smallest box that holds me
    auto envelope() const -> envelope_type;

    // implementation details - data
private:
    rings_type _rings;
};


// get the inline definitions
#include "Polygon.icc"


// end of file
