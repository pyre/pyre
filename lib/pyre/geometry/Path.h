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


// a path on the sphere: a sequence of vertices joined by edges, which are either geodesics, the
// shorter arcs of the great circles through their ends, or straight lines in the chart; the
// relations see a path as the great-circle arcs that join the points it traces, which are its
// vertices when its edges are geodesic, and pieces of its edges when they are straight in the
// chart
template <class chartT>
class pyre::geometry::Path {
    // type aliases
public:
    // me
    using self_type = Path<chartT>;
    // my chart
    using chart_type = chartT;
    // its space
    using space_type = typename chart_type::space_type;
    // and its points
    using point_type = Point<space_type>;
    // my vertices
    using vertices_type = std::vector<point_type>;
    // the points i trace
    using arcs_type = std::vector<spherical::vector_t>;
    // the smallest shape of the chart that holds me
    using envelope_type = Box<chart_type>;

    // metamethods
public:
    // the path through {vertices}, with {geodesic} edges or edges straight in the chart
    Path(const vertices_type & vertices, bool geodesic = true);

    // the rest
    Path(const Path &) = default;
    Path(Path &&) = default;
    Path & operator=(const Path &) = default;
    Path & operator=(Path &&) = default;
    ~Path() = default;

    // equality: paths through the same vertices, with the same kind of edges
    auto operator==(const Path & other) const -> bool;

    // interface
public:
    // my vertices
    auto vertices() const -> const vertices_type &;
    // whether my edges are geodesics
    auto geodesic() const -> bool;
    // the points i trace, in order, joined by great-circle arcs
    auto arcs() const -> const arcs_type &;
    // whether the point {p} is on me
    auto contains(const point_type & p) const -> bool;
    // the smallest box that holds me
    auto envelope() const -> envelope_type;

    // implementation details - data
private:
    vertices_type _vertices;
    bool _geodesic;
    arcs_type _arcs;
};


// get the inline definitions
#include "Path.icc"


// end of file
