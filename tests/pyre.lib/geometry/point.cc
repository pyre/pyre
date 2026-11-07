// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// config
#include <portinfo>
// externals
#include <pyre/journal.h>
#include <pyre/geometry.h>

// main
int
main()
{
    // type alias
    using point3d_t = pyre::geometry::point_t<pyre::geometry::euclidean_t<3>>;
    // make a point
    point3d_t p { 0., 0., 0. };

    // make a channel
    pyre::journal::debug_t info("pyre.geometry");
    // show me
    info << pyre::journal::at() << "point: (" << p << ")" << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
