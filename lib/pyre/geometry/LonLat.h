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


// longitude and latitude, in degrees, on a surface whose points are unit normals: the sphere,
// where the latitude is geocentric, and the ellipsoid, where it is geodetic; on both, the
// latitude is the angle between the normal and the equatorial plane, so the map is the same;
// the poles and the antimeridian are properties of this chart, not of the surface
template <class spaceT>
class pyre::geometry::LonLat {
    // type aliases
public:
    // me
    using self_type = LonLat<spaceT>;
    // my space
    using space_type = spaceT;
    using point_type = Point<space_type>;
    // my coordinates: longitude and latitude, in that order
    using coordinates_type = std::array<double, 2>;

    // metamethods
public:
    constexpr LonLat() = default;
    constexpr LonLat(const LonLat &) = default;
    constexpr LonLat(LonLat &&) = default;
    constexpr LonLat & operator=(const LonLat &) = default;
    constexpr LonLat & operator=(LonLat &&) = default;
    constexpr ~LonLat() = default;

    // equality
    constexpr auto operator==(const LonLat &) const -> bool = default;

    // interface
public:
    // the point with the given longitude and latitude
    auto point(const coordinates_type & coordinates) const -> point_type;
    // the longitude and latitude of the given point
    auto coordinates(const point_type & p) const -> coordinates_type;
};


// get the inline definitions
#include "LonLat.icc"


// end of file
