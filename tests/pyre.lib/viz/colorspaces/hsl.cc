// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// STL
#include <iostream>
// support
#include <pyre/viz.h>


// type aliases
using rgb_t = pyre::viz::rgb_t;


// driver
int
main(int argc, char * argv[])
{
    // name some colors
    // the edges
    rgb_t black { 0, 0, 0 };
    rgb_t white { 1, 1, 1 };
    // the primaries
    rgb_t red { 1, 0, 0 };
    // rgb_t green { 0, 1, 0 };
    rgb_t blue { 0, 0, 1 };

    // check the primaries
    assert((pyre::viz::colorspaces::hsl(0, 1, 0.5) == red));
    // green is good only within machine epsilon, so either a better {==} is required
    // or the kernel has to round its results to fewer significant figures
    // assert((pyre::viz::colorspaces::hsl(2 * M_PI / 3, 1, 0.5) == green));
    assert((pyre::viz::colorspaces::hsl(4 * M_PI / 3, 1, 0.5) == blue));

    // anything at zero brightness should be black
    assert((pyre::viz::colorspaces::hsl(0, 0, 0) == black));
    assert((pyre::viz::colorspaces::hsl(2 * M_PI / 3, 0, 0) == black));
    assert((pyre::viz::colorspaces::hsl(4 * M_PI / 3, 0, 0) == black));
    assert((pyre::viz::colorspaces::hsl(0, 1, 0) == black));
    assert((pyre::viz::colorspaces::hsl(2 * M_PI / 3, 1, 0) == black));
    assert((pyre::viz::colorspaces::hsl(4 * M_PI / 3, 1, 0) == black));

    // anything at full brightness should be white
    assert((pyre::viz::colorspaces::hsl(0, 0, 1) == white));
    assert((pyre::viz::colorspaces::hsl(2 * M_PI / 3, 0, 1) == white));
    assert((pyre::viz::colorspaces::hsl(4 * M_PI / 3, 0, 1) == white));
    assert((pyre::viz::colorspaces::hsl(0, 1, 1) == white));
    assert((pyre::viz::colorspaces::hsl(2 * M_PI / 3, 1, 1) == white));
    assert((pyre::viz::colorspaces::hsl(4 * M_PI / 3, 1, 1) == white));

    // all done
    return 0;
}


// end of file
