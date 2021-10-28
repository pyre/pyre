// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_colorspaces_hsb_h)
#define pyre_viz_colorspaces_hsb_h


// the HSB to RGB conversion kernel
// see the wikipedia article at {https://en.wikipedia.org/wiki/HSL_and_HSV#HSB_to_RGB}
auto
pyre::viz::colorspaces::hsb(double h, double s, double b) -> rgb_t
{
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
