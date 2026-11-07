// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a reference system carries its space, its chart and its authority code


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::ellipsoid_t;
using chart_t = pyre::geometry::lonlat_t<space_t>;
using system_t = pyre::geometry::referencesystem_t<chart_t>;


// driver
int
main()
{
    // longitude and latitude on the WGS84 ellipsoid
    auto wgs84 = system_t(space_t::wgs84(), chart_t(), "EPSG", 4326);

    // carries its parts
    assert(wgs84.space() == space_t::wgs84());
    assert(wgs84.authority() == "EPSG");
    assert(wgs84.code() == 4326);
    // and its chart maps points
    auto p = wgs84.chart().point({ 0.0, 0.0 });
    assert(p[0] == 1.0);

    // all done
    return 0;
}


// end of file
