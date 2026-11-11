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


// the sphere of a given radius: its points are the unit vectors of the directions from its
// center, which have no singularities at the poles or across the antimeridian, and its
// geodesics are the great circles
class pyre::geometry::Sphere {
    // type aliases
public:
    // me
    using self_type = Sphere;
    // my points
    using rep_type = std::array<double, 3>;
    using point_type = Point<self_type>;
    // distances
    using distance_type = double;
    // indices
    using size_type = size_t;
    // the hashes of my points
    using hash_type = hash_t;

    // metamethods
public:
    // a sphere of the given radius, by default the unit sphere
    constexpr explicit Sphere(double radius = 1.0);

    // the rest
    constexpr Sphere(const Sphere &) = default;
    constexpr Sphere(Sphere &&) = default;
    constexpr Sphere & operator=(const Sphere &) = default;
    constexpr Sphere & operator=(Sphere &&) = default;
    constexpr ~Sphere() = default;

    // equality: spheres of the same radius are the same space
    constexpr auto operator==(const Sphere &) const -> bool = default;

    // interface
public:
    // my dimension
    static constexpr auto dimension() -> size_type;
    // my radius
    constexpr auto radius() const -> double;
    // the length of the shorter great circle arc between two points
    auto distance(const point_type & p, const point_type & q) const -> distance_type;
    // the central angle between two points, in radians
    static auto angle(const point_type & p, const point_type & q) -> double;

    // rendering
public:
    // write a point as the components of its unit vector
    static auto inject(std::ostream & stream, const rep_type & p) -> void;

    // hashing
public:
    // the hash of a point, shared by the points that compare equal
    static auto hash(const rep_type & p) -> hash_type;

    // implementation details - data
private:
    double _radius;
};


// get the inline definitions
#include "Sphere.icc"


// end of file
