// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colorspaces_hsl_h)
#define pyre_viz_colorspaces_hsl_h


// the HSL to RGB conversion kernel
// see the wikipedia article at {https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB}
// N.B.:
//   h in [-pi, pi] radians
//   s in [0, 1]
//   l in [0, 1]
auto
pyre::viz::colorspaces::hsl(double h, double s, double l) -> viz::rgb_t
{
    // convert the hue from radians to degrees
    h *= 180 / M_PI;
    // rescale the saturation
    auto a = s * std::min(l, 1 - l);
    // build the kernel
    auto f = [=](double n) -> double {
        auto k = std::fmod((n + h / 30), 12);
        auto v = l - a * std::max(-1.0, std::min({ k - 3, 9 - k, 1.0 }));
        return v;
    };

    // pack and return
    return { f(0), f(8), f(4) };
}


#endif

// end of file
