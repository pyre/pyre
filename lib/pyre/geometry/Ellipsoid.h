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


// the oblate spheroid of a given semi-major axis and flattening: its points are the unit
// normals to its surface, which have no singularities at the poles or across the antimeridian
class pyre::geometry::Ellipsoid {
    // type aliases
public:
    // me
    using self_type = Ellipsoid;
    // my points
    using rep_type = std::array<double, 3>;
    using point_type = Point<self_type>;
    // indices
    using size_type = size_t;

    // metamethods
public:
    // an ellipsoid with the given semi-major axis and flattening
    constexpr Ellipsoid(double semimajor, double flattening);

    // the rest
    constexpr Ellipsoid(const Ellipsoid &) = default;
    constexpr Ellipsoid(Ellipsoid &&) = default;
    constexpr Ellipsoid & operator=(const Ellipsoid &) = default;
    constexpr Ellipsoid & operator=(Ellipsoid &&) = default;
    constexpr ~Ellipsoid() = default;

    // equality: ellipsoids with the same axes are the same space
    constexpr auto operator==(const Ellipsoid &) const -> bool = default;

    // the ellipsoid of the world geodetic system of 1984
    static constexpr auto wgs84() -> Ellipsoid;

    // interface
public:
    // my dimension
    static constexpr auto dimension() -> size_type;
    // the semi-major axis, the equatorial radius
    constexpr auto semimajor() const -> double;
    // the semi-minor axis, the polar radius
    constexpr auto semiminor() const -> double;
    // the flattening
    constexpr auto flattening() const -> double;
    // the square of the eccentricity
    constexpr auto squaredEccentricity() const -> double;

    // rendering
public:
    // write a point as the components of its unit normal
    static auto inject(std::ostream & stream, const rep_type & p) -> void;

    // implementation details - data
private:
    double _semimajor;
    double _flattening;
};


// get the inline definitions
#include "Ellipsoid.icc"


// end of file
