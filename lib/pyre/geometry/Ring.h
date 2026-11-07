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
#include "spherical.h"
#include "Box.h"


// a ring on the sphere: a closed sequence of vertices joined by edges, which are either
// geodesics or straight lines in the chart, and the region it bounds
//
// a ring divides the sphere into two regions, and nothing about the ring alone says which one it
// means: a small ring around a city bounds the city, and it also bounds the rest of the earth;
// the ring bounds the region to its left, as one walks along it from vertex to vertex, seen from
// outside the sphere; this is the only rule that can describe every region, including the ones
// larger than a hemisphere, and walking the same ring the other way describes the complement
//
// the rule is unforgiving: a ring walked the wrong way describes the complement of what was
// meant; data whose convention is known is read with it and reversed when it disagrees, and
// rings drawn or typed by people, which come in either direction, go through {orient}, which
// walks a ring so that it bounds the smaller of its two regions; see the section on regions on
// the sphere in doc/design/geometry.md
//
// the ring keeps a few reference points and the side of each, settled once when it is made; any
// other point is on the side of a reference unless the arc between them crosses the ring an odd
// number of times; the ring is a closed set, so the points on it are inside
template <class chartT>
class pyre::geometry::Ring {
    // type aliases
public:
    // me
    using self_type = Ring<chartT>;
    // my chart
    using chart_type = chartT;
    // its space
    using space_type = typename chart_type::space_type;
    // and its points
    using point_type = Point<space_type>;
    // my vertices
    using vertices_type = std::vector<point_type>;
    // the points of the space around the sphere
    using vector_type = spherical::vector_t;
    // the points i trace
    using arcs_type = std::vector<vector_type>;
    // the smallest shape of the chart that holds the region i bound
    using envelope_type = Box<chart_type>;

    // metamethods
public:
    // the ring through {vertices}, with {geodesic} edges or edges straight in the chart; the ring
    // closes itself, so its last vertex need not repeat its first
    Ring(const vertices_type & vertices, bool geodesic = true);

    // the rest
    Ring(const Ring &) = default;
    Ring(Ring &&) = default;
    Ring & operator=(const Ring &) = default;
    Ring & operator=(Ring &&) = default;
    ~Ring() = default;

    // equality: rings through the same vertices, in the same order, with the same kind of edges
    auto operator==(const Ring & other) const -> bool;

    // interface
public:
    // my vertices
    auto vertices() const -> const vertices_type &;
    // whether my edges are geodesics
    auto geodesic() const -> bool;
    // the points i trace, in order, joined by great-circle arcs, back to where i start
    auto arcs() const -> const arcs_type &;
    // whether the point {p} is on me, within the tolerance of the arcs
    auto boundary(const point_type & p) const -> bool;
    // whether the point {p} is in the region i bound, which includes me
    auto contains(const point_type & p) const -> bool;
    // the area of the region i bound, in steradians on the unit sphere
    auto area() const -> double;
    // the ring through my vertices in the opposite order, which bounds the other region
    auto reversed() const -> self_type;
    // the smallest box that holds the region i bound
    auto envelope() const -> envelope_type;

    // implementation details
private:
    // a point whose side is known
    struct reference_t {
        // the point
        vector_type point;
        // and whether it is in the region i bound
        bool inside;
    };
    // the references
    using references_type = std::vector<reference_t>;

    // whether the point {p} is on me
    auto touches(const vector_type & p) const -> bool;
    // the side of the point {p}, counted from {reference}; nothing when the arc between them
    // passes through one of the points i trace, which makes the count unreliable
    auto side(const vector_type & p, const reference_t & reference) const -> std::optional<bool>;
    // settle the side of the candidate references
    auto settle() const -> references_type;

    // implementation details - data
private:
    vertices_type _vertices;
    bool _geodesic;
    arcs_type _arcs;
    references_type _references;
};


// get the inline definitions
#include "Ring.icc"


// end of file
