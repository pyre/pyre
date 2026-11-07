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


// the predicates of geometry on the unit sphere, on the unit vectors that stand for its points;
// a geodesic edge is the shorter arc of the great circle through its ends, and every decision
// reduces to the side of a great circle a point is on, the sign of a determinant of three unit
// vectors; that sign is computed in double precision, and again in twice the precision when the
// first result is too close to zero to be trusted; only a determinant that is still within the
// rounding error of the second pass counts as zero
//
// whether a point is on an arc is a different question: a point on a great circle can only be
// computed to within rounding, so a point placed on an edge is almost never exactly on it, and
// the edges of two shapes that share a boundary don't exactly coincide; a point counts as on an
// arc when it is within {tolerance} of it; shapes are closed sets, so a point on a boundary
// belongs to the shape, and shapes whose boundaries come that close touch
namespace pyre::geometry::spherical {
    // a unit vector, or any vector in the space around the sphere
    using vector_t = std::array<double, 3>;

    // the algebra of vectors
    // the dot product
    inline auto dot(const vector_t & a, const vector_t & b) -> double;
    // the cross product
    inline auto cross(const vector_t & a, const vector_t & b) -> vector_t;
    // the vector scaled to unit length
    inline auto normalize(const vector_t & a) -> vector_t;

    // the side of the great circle through {a} and {b} that {c} is on: +1 to the left, as one
    // walks from {a} to {b} seen from outside the sphere, -1 to the right, and 0 when even twice
    // the precision of a double can't tell
    inline auto orientation(const vector_t & a, const vector_t & b, const vector_t & c) -> int;

    // whether the directions from {o} toward {a}, {b} and {c} come in that order as one turns
    // counterclockwise around {o}, seen from outside the sphere
    inline auto ordered(
        const vector_t & a, const vector_t & b, const vector_t & c, const vector_t & o) -> bool;

    // whether {p} lies on the arc from {a} to {b}, ends included, within {tolerance}
    inline auto onArc(const vector_t & a, const vector_t & b, const vector_t & p) -> bool;
    // whether the arcs from {a} to {b} and from {c} to {d} share a point, ends included
    inline auto meets(
        const vector_t & a, const vector_t & b, const vector_t & c, const vector_t & d) -> bool;
    // whether the arcs from {a} to {b} and from {c} to {d} cross at a point inside both; arcs
    // that only touch, or meet at an end of either, don't
    inline auto crosses(
        const vector_t & a, const vector_t & b, const vector_t & c, const vector_t & d) -> bool;

    // whether any arc of the chain {a} meets any arc of the chain {b}, ends included; a chain is
    // a sequence of points joined by great-circle arcs, and a chain of a single point is that point
    inline auto meets(const std::vector<vector_t> & a, const std::vector<vector_t> & b) -> bool;

    // the latitude of the northernmost point of the arc from {a} to {b}, in radians
    inline auto highest(const vector_t & a, const vector_t & b) -> double;
    // and of its southernmost point
    inline auto lowest(const vector_t & a, const vector_t & b) -> double;

    // the points along a sequence of {vertices}, in order, close enough to each other to be
    // joined by great-circle arcs: the vertices themselves when the edges are {geodesic}, and
    // pieces of the edges no longer than {chartPiece} in either coordinate when the edges are
    // straight in the {chart}; a {closed} sequence returns to its first vertex at the end; an
    // edge straight in the chart takes the shorter way around in longitude
    template <class chartT>
    inline auto trace(
        const chartT & chart, const std::vector<Point<typename chartT::space_type>> & vertices,
        bool geodesic, bool closed) -> std::vector<vector_t>;

    // the distance, in radians, within which a point counts as on an arc: about six microns on
    // the earth, far beyond the rounding of a computed point and far below any distance that
    // matters on the ground
    inline constexpr auto tolerance = 1e-12;

    // the longest piece, in degrees of either coordinate, into which an edge straight in the
    // chart is cut, so that great-circle arcs can stand for it; the arc departs from the edge by
    // a few meters at most
    inline constexpr auto chartPiece = 0.25;

    // arithmetic in twice the precision of a double, which the orientation falls back on when
    // double precision can't tell: a value is the unevaluated sum of a large part and a small
    // one, and each step keeps its rounding error in the small part
    struct twofold_t {
        // the large part
        double high;
        // and the rounding error of the large part
        double low;
    };
    // the exact sum of two doubles, when the first is the larger
    inline auto quickSum(double a, double b) -> twofold_t;
    // the exact sum of two doubles
    inline auto twoSum(double a, double b) -> twofold_t;
    // the exact product of two doubles
    inline auto twoProduct(double a, double b) -> twofold_t;
    // the sum of two values in twice the precision
    inline auto add(const twofold_t & a, const twofold_t & b) -> twofold_t;
    // the difference of the products {a b} and {c d}, in twice the precision
    inline auto productDifference(double a, double b, double c, double d) -> twofold_t;
    // the product of a value in twice the precision and a double
    inline auto scale(const twofold_t & a, double b) -> twofold_t;

    // the north pole
    inline constexpr auto north = vector_t { 0.0, 0.0, 1.0 };
    // and the south pole
    inline constexpr auto south = vector_t { 0.0, 0.0, -1.0 };
} // namespace pyre::geometry::spherical


// get the inline definitions
#include "spherical.icc"


// end of file
