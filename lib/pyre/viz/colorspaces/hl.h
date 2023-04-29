// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colorspaces_hl_h)
#define pyre_viz_colorspaces_hl_h


// the HL to RGB conversion kernel
// the kernel maps two values, hue and luminosity to RGB using a colorpmap that is
// designed for displaying complex values [zebker@stanford.edu, private communication]
auto
pyre::viz::colorspaces::hl(double h, double l, double threshold) -> viz::rgb_t
{
    // 2 * π / 3
    const auto angle = 2 * M_PI / 3;

    // forward map negative hues
    if (h < 0) {
        // to [π, 2π]
        h += 2 * M_PI;
    }

    // deduce the colorwheel region by comparing against the dominant axes
    int axis = h / angle;
    // and the mixing scale as a linear interpolation between the other two axes
    auto mix = std::fmod(h, angle) / angle;

    // we mix three values
    // the color dual to the dominant region is at whatever value the user supplied
    auto dual = l;
    // the color at the low end of the region
    auto low = l * (threshold + (1 - threshold) * mix);
    // and the color at the high end of the region
    auto high = l * (threshold + (1 - threshold) * (1 - mix));
    // place them in a vector
    double wheel[] = { low, high, dual };
    // and convert to {rgb_t}
    return { wheel[(3 - axis) % 3], wheel[(4 - axis) % 3], wheel[(5 - axis) % 3] };
}


#endif

// end of file
