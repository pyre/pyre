// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colorspaces_hsb_h)
#define pyre_viz_colorspaces_hsb_h


// the HSB to RGB conversion kernel
// see the wikipedia article at {https://en.wikipedia.org/wiki/HSL_and_HSV#HSB_to_RGB}
// N.B.:
//   h in [-pi, pi] radians
//   s in [0, 1]
//   b in [0, 1]
auto
pyre::viz::colorspaces::hsb(double h, double s, double b) -> viz::rgb_t
{
    // convert the hue from radians to degrees
    h *= 180 / M_PI;
    // build the kernel
    auto f = [=](double n) -> double {
        auto k = std::fmod((n + h / 60), 6);
        auto a = s * std::max(0.0, std::min({ k, 4 - k, 1.0 }));
        auto v = b * (1 - a);
        return v;
    };

    // pack and return
    return { f(5), f(3), f(1) };
}


#endif

// end of file
