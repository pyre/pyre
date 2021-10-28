// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_api_h)
#define pyre_viz_api_h


// publicly visible types
namespace pyre::viz {

    // codecs
    // microsoft bmp
    using bmp_t = BMP;

} // namespace pyre::viz


// conversions from other color spaces to {rgb}
namespace pyre::viz::colorspaces {
    auto hsb(double h, double s, double b) -> rgb_t;
    auto hsl(double h, double s, double l) -> rgb_t;
} // namespace pyre::viz::colorspaces


#endif

// end of file
