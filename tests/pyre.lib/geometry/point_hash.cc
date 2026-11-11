// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal points hash alike in every space that knows how to hash its points, that the
// two zeros of a coordinate hash alike since they compare equal, and that the order of the
// coordinates shapes the hash


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using plane_t = pyre::geometry::euclidean_t<2>;
using lattice_t = pyre::geometry::lattice_t<2>;
using sphere_t = pyre::geometry::sphere_t;
using timeline_t = pyre::geometry::timeline_t;
using height_t = pyre::geometry::euclidean_t<1>;
using column_t = pyre::geometry::product_t<sphere_t, height_t>;


// driver
int
main()
{
    // a point of the plane
    using planar_t = pyre::geometry::point_t<plane_t>;
    // hashes like another made the same way
    assert(planar_t(1.0, 2.0).hash() == planar_t(1.0, 2.0).hash());
    // the two zeros compare equal
    assert(planar_t(0.0, -0.0) == planar_t(0.0, 0.0));
    // so they hash alike
    assert(planar_t(0.0, -0.0).hash() == planar_t(0.0, 0.0).hash());
    // and swapping the coordinates makes a different point, with a different hash
    assert(planar_t(1.0, 2.0).hash() != planar_t(2.0, 1.0).hash());

    // a node of the lattice
    using node_t = pyre::geometry::point_t<lattice_t>;
    // hashes like another made the same way
    assert(node_t(3L, 4L).hash() == node_t(3L, 4L).hash());
    // and not like its mirror
    assert(node_t(3L, 4L).hash() != node_t(4L, 3L).hash());

    // a point of the sphere
    using place_t = pyre::geometry::point_t<sphere_t>;
    // hashes like another made the same way
    assert(place_t(0.0, 0.0, 1.0).hash() == place_t(0.0, 0.0, 1.0).hash());
    // and not like a different direction
    assert(place_t(0.0, 0.0, 1.0).hash() != place_t(1.0, 0.0, 0.0).hash());

    // an instant of the timeline
    using instant_t = pyre::geometry::point_t<timeline_t>;
    // hashes like another made the same way
    assert(instant_t(3600.0).hash() == instant_t(3600.0).hash());

    // a point of a product hashes its parts the way its factors do
    using position_t = pyre::geometry::point_t<column_t>;
    // so two made the same way
    auto p = position_t(place_t(1.0, 0.0, 0.0), pyre::geometry::point_t<height_t>(100.0));
    auto q = position_t(place_t(1.0, 0.0, 0.0), pyre::geometry::point_t<height_t>(100.0));
    // hash alike
    assert(p.hash() == q.hash());

    // all done
    return 0;
}


// end of file
