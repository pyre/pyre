// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal paths hash alike, and that paths through the same vertices with different
// kinds of edges hash differently, since they are different paths


// portability
#include <portinfo>
// STL
#include <cassert>
#include <vector>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using path_t = pyre::geometry::path_t<chart_t>;


// driver
int
main()
{
    // the chart
    auto chart = chart_t();
    // the point at a longitude and a latitude
    auto at = [&chart](double longitude, double latitude) {
        // place it
        return chart.point({ longitude, latitude });
    };
    // the vertices of a path along the parallel at 45 degrees north
    auto vertices = std::vector { at(0, 45), at(30, 45), at(60, 45) };

    // a path through them
    auto path = path_t(vertices);
    // hashes like another made the same way
    assert(path.hash() == path_t(vertices).hash());
    // the path that follows the parallel instead of the great circles
    auto parallel = path_t(vertices, false);
    // is a different path
    assert(path != parallel);
    // with a different hash
    assert(path.hash() != parallel.hash());

    // all done
    return 0;
}


// end of file
