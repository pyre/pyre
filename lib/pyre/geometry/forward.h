// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "externals.h"


// forward declarations
namespace pyre::geometry {
    // local type aliases
    using size_t = std::size_t;
    using string_t = std::string;

    // spaces
    // the euclidean space of a given dimension
    template <size_t dim>
    class Euclidean;
    // the sphere of a given radius
    class Sphere;
    // the oblate spheroid
    class Ellipsoid;
    // the affine line of time
    class Timeline;
    // finite subsets of the integer lattice
    template <size_t dim>
    class Lattice;
    // the cartesian product of two spaces
    template <class firstT, class secondT>
    class Product;

    // the elements of a space
    template <class spaceT>
    class Point;

    // charts
    // the identity chart of euclidean space
    template <size_t dim>
    class Cartesian;
    // longitude and latitude on the sphere and the ellipsoid
    template <class spaceT>
    class LonLat;

    // a space with a chart and an authority code
    template <class chartT>
    class ReferenceSystem;

    // point cloud
    template <typename pointT>
    class PointCloud;
    // brick
    template <size_t dim, typename nodeT>
    class Brick;
} // namespace pyre::geometry


// operators
namespace pyre::geometry {
    // stream injection: overload the global operator<<
    // points
    template <class spaceT>
    inline auto operator<<(std::ostream & stream, const Point<spaceT> & point) -> std::ostream &;
    // bricks
    template <size_t dim, typename nodeT>
    inline auto & operator<<(std::ostream & stream, const Brick<dim, nodeT> & brick);

    // operators on bricks
    // equality
    template <size_t dim, typename nodeT>
    inline auto operator==(const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
    // inequality
    template <size_t dim, typename nodeT>
    inline auto operator!=(const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
} // namespace pyre::geometry


// end of file
