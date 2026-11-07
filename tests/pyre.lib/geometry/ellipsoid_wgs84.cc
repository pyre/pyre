// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the axes and the eccentricity of the WGS84 ellipsoid against their published values


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::ellipsoid_t;


// driver
int
main()
{
    // the ellipsoid, built at compile time
    constexpr auto wgs84 = space_t::wgs84();

    // the equatorial radius is a defining constant
    static_assert(wgs84.semimajor() == 6378137.0);
    // the polar radius is derived; the published value is 6356752.314245 m
    assert(std::abs(wgs84.semiminor() - 6356752.314245) < 1e-6);
    // and so is the square of the eccentricity, published as 6.69437999014e-3
    assert(std::abs(wgs84.squaredEccentricity() - 6.69437999014e-3) < 1e-14);
    // the ellipsoid is a surface
    static_assert(space_t::dimension() == 2);

    // all done
    return 0;
}


// end of file
