// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::geometry}
#include "forward.h"


// type aliases
namespace pyre::geometry {
    // spaces
    template <size_t dim = 3>
    using euclidean_t = Euclidean<dim>;
    using sphere_t = Sphere;
    using ellipsoid_t = Ellipsoid;
    using timeline_t = Timeline;
    template <size_t dim>
    using lattice_t = Lattice<dim>;
    template <class firstT, class secondT>
    using product_t = Product<firstT, secondT>;

    // points
    template <class spaceT = euclidean_t<3>>
    using point_t = Point<spaceT>;

    // charts
    template <size_t dim = 3>
    using cartesian_t = Cartesian<dim>;
    template <class spaceT = ellipsoid_t>
    using lonlat_t = LonLat<spaceT>;

    // reference systems
    template <class chartT>
    using referencesystem_t = ReferenceSystem<chartT>;

    // shapes
    template <class lineT = timeline_t>
    using interval_t = Interval<lineT>;
    template <class shapeT>
    using collection_t = Collection<shapeT>;

    // point cloud
    template <typename pointT = point_t<>>
    using cloud_t = PointCloud<pointT>;
    // brick
    template <size_t dim = 3, typename nodeT = point_t<>>
    using brick_t = Brick<dim, nodeT>;
} // namespace pyre::geometry


// end of file
