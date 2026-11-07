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


// the euclidean space of dimension {dim}: its points are arrays of coordinates, its straight
// lines are the geodesics, and its points subtract to give vectors
template <std::size_t dim>
class pyre::geometry::Euclidean {
    // type aliases
public:
    // me
    using self_type = Euclidean<dim>;
    // my coordinates
    using coordinate_type = double;
    // my points
    using rep_type = std::array<coordinate_type, dim>;
    using point_type = Point<self_type>;
    // the vectors between my points
    using vector_type = std::array<coordinate_type, dim>;
    // distances
    using distance_type = double;
    // indices
    using size_type = size_t;

    // metamethods
public:
    constexpr Euclidean() = default;
    constexpr Euclidean(const Euclidean &) = default;
    constexpr Euclidean(Euclidean &&) = default;
    constexpr Euclidean & operator=(const Euclidean &) = default;
    constexpr Euclidean & operator=(Euclidean &&) = default;
    constexpr ~Euclidean() = default;

    // equality: all euclidean spaces of the same dimension are the same space
    constexpr auto operator==(const Euclidean &) const -> bool = default;

    // interface
public:
    // my dimension
    static constexpr auto dimension() -> size_type;
    // the length of the straight segment between two points
    constexpr auto distance(const point_type & p, const point_type & q) const -> distance_type;

    // the affine structure
public:
    // the vector from {q} to {p}
    static constexpr auto difference(const rep_type & p, const rep_type & q) -> vector_type;
    // the point {p} translated by {v}
    static constexpr auto translate(const rep_type & p, const vector_type & v) -> rep_type;
    // the opposite of {v}
    static constexpr auto opposite(const vector_type & v) -> vector_type;

    // the order of the line, when i am one
public:
    // the coordinate of a point of the line
    static constexpr auto coordinate(const rep_type & p) -> coordinate_type
        requires(dim == 1);
    // the point of the line at the given coordinate
    static constexpr auto fromCoordinate(coordinate_type x) -> rep_type
        requires(dim == 1);

    // rendering
public:
    // write a point as its comma separated coordinates
    static auto inject(std::ostream & stream, const rep_type & p) -> void;
};


// get the inline definitions
#include "Euclidean.icc"


// end of file
