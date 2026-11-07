// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check which spaces satisfy which concepts: the spaces with an affine structure, the ones with
// a metric, and the charts


// portability
#include <portinfo>
// support
#include <pyre/geometry.h>


// alias the namespace
namespace geometry = pyre::geometry;


// every space is a space
static_assert(geometry::space_c<geometry::euclidean_t<3>>);
static_assert(geometry::space_c<geometry::sphere_t>);
static_assert(geometry::space_c<geometry::ellipsoid_t>);
static_assert(geometry::space_c<geometry::timeline_t>);
static_assert(geometry::space_c<geometry::lattice_t<2>>);
static_assert(geometry::space_c<geometry::product_t<geometry::ellipsoid_t, geometry::timeline_t>>);

// euclidean space and the timeline are affine
static_assert(geometry::affine_space_c<geometry::euclidean_t<3>>);
static_assert(geometry::affine_space_c<geometry::timeline_t>);
// but the curved surfaces and the lattice are not
static_assert(not geometry::affine_space_c<geometry::sphere_t>);
static_assert(not geometry::affine_space_c<geometry::ellipsoid_t>);
static_assert(not geometry::affine_space_c<geometry::lattice_t<2>>);

// euclidean space, the sphere and the timeline measure distances
static_assert(geometry::metric_space_c<geometry::euclidean_t<3>>);
static_assert(geometry::metric_space_c<geometry::sphere_t>);
static_assert(geometry::metric_space_c<geometry::timeline_t>);
// the ellipsoid does not, yet, and the lattice has no metric
static_assert(not geometry::metric_space_c<geometry::ellipsoid_t>);
static_assert(not geometry::metric_space_c<geometry::lattice_t<2>>);

// the charts are charts
static_assert(geometry::chart_c<geometry::cartesian_t<2>>);
static_assert(geometry::chart_c<geometry::lonlat_t<geometry::sphere_t>>);
static_assert(geometry::chart_c<geometry::lonlat_t<geometry::ellipsoid_t>>);


// driver
int
main()
{
    // the checks happen at compile time
    return 0;
}


// end of file
