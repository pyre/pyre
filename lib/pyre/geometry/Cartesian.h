// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "Euclidean.h"


// the identity chart of the euclidean space of dimension {dim}: the coordinates of a point are
// the ones it stores
template <std::size_t dim>
class pyre::geometry::Cartesian {
    // type aliases
public:
    // me
    using self_type = Cartesian<dim>;
    // my space
    using space_type = Euclidean<dim>;
    using point_type = Point<space_type>;
    // my coordinates
    using coordinates_type = typename space_type::rep_type;

    // metamethods
public:
    constexpr Cartesian() = default;
    constexpr Cartesian(const Cartesian &) = default;
    constexpr Cartesian(Cartesian &&) = default;
    constexpr Cartesian & operator=(const Cartesian &) = default;
    constexpr Cartesian & operator=(Cartesian &&) = default;
    constexpr ~Cartesian() = default;

    // equality
    constexpr auto operator==(const Cartesian &) const -> bool = default;

    // interface
public:
    // the point with the given coordinates
    constexpr auto point(const coordinates_type & coordinates) const -> point_type;
    // the coordinates of the given point
    constexpr auto coordinates(const point_type & p) const -> coordinates_type;
};


// get the inline definitions
#include "Cartesian.icc"


// end of file
