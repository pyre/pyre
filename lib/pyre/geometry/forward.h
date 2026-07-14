// -*- C++ -*-
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
    typedef std::size_t size_t;
    // point
    template <size_t dim, typename dataT>
    class Point;
    // point cloud
    template <typename pointT>
    class PointCloud;
    // brick
    template <size_t dim, typename nodeT>
    class Brick;
} // namespace pyre::geometry


// type aliases for the above
namespace pyre::geometry {
    // point
    template <size_t dim = 3, typename dataT = double>
    using point_t = Point<dim, dataT>;
    // point cloud
    template <typename pointT = point_t<3, double>>
    using cloud_t = PointCloud<pointT>;
    // brick
    template <size_t dim = 3, typename nodeT = point_t<3>>
    using brick_t = Brick<dim, nodeT>;
} // namespace pyre::geometry


// operators
namespace pyre::geometry {
    // operators on points
    // equality
    template <size_t dim, typename dataT>
    inline auto operator==(const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);
    // inequality
    template <size_t dim, typename dataT>
    inline auto operator!=(const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);

    // operators on bricks
    // equality
    template <size_t dim, typename nodeT>
    inline auto operator==(const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
    // inequality
    template <size_t dim, typename nodeT>
    inline auto operator!=(const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);

    // stream injection: overload the global operator<<
    // points
    template <size_t dim, typename dataT>
    inline auto & operator<<(std::ostream & stream, const Point<dim, dataT> & point);
    // bricks
    template <size_t dim, typename nodeT>
    inline auto & operator<<(std::ostream & stream, const Brick<dim, nodeT> & brick);
} // namespace pyre::geometry


// end of file
