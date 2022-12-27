// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
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
    rgb_t green { 0, 1, 0 };
    rgb_t blue { 0, 0, 1 };

    // check the primaries
    assert((pyre::viz::colorspaces::hsb(0, 1, 1) == red));
    assert((pyre::viz::colorspaces::hsb(2 * M_PI / 3, 1, 1) == green));
    assert((pyre::viz::colorspaces::hsb(4 * M_PI / 3, 1, 1) == blue));

    // anything at zero brightness should be black
    assert((pyre::viz::colorspaces::hsb(0, 0, 0) == black));
    assert((pyre::viz::colorspaces::hsb(2 * M_PI / 3, 0, 0) == black));
    assert((pyre::viz::colorspaces::hsb(4 * M_PI / 3, 0, 0) == black));
    assert((pyre::viz::colorspaces::hsb(0, 1, 0) == black));
    assert((pyre::viz::colorspaces::hsb(2 * M_PI / 3, 1, 0) == black));
    assert((pyre::viz::colorspaces::hsb(4 * M_PI / 3, 1, 0) == black));

    // anything at zero saturation and full brightness should be white
    assert((pyre::viz::colorspaces::hsb(0, 0, 1) == white));
    assert((pyre::viz::colorspaces::hsb(2 * M_PI / 3, 0, 1) == white));
    assert((pyre::viz::colorspaces::hsb(4 * M_PI / 3, 0, 1) == white));

    // all done
    return 0;
}


// end of file
