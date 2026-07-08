// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// the opt-in color palette, which maps a name to a color
#include <pyre/chroma/rgb/palette.h>


// bind the {rgb} converters and the color palette
void
pyre::py::chroma::rgb(py::module & m)
{
    // create the {rgb} submodule
    auto rgb = m.def_submodule(
        // the name of the module
        "rgb",
        // its docstring
        "converters that assemble an {rgb} color from another color space");

    // from {hsl}
    rgb.def(
        // the name
        "hsl",
        // the converter
        &pyre::chroma::rgb::hsl,
        // the signature
        "hue"_a, "saturation"_a, "luminosity"_a,
        // the docstring
        "make a color from an {hsl} triplet");
    // from {hsb}
    rgb.def(
        // the name
        "hsb",
        // the converter
        &pyre::chroma::rgb::hsb,
        // the signature
        "hue"_a, "saturation"_a, "brightness"_a,
        // the docstring
        "make a color from an {hsb} triplet");
    // from {hl}
    rgb.def(
        // the name
        "hl",
        // the converter
        &pyre::chroma::rgb::hl,
        // the signature, carrying the same default mixing threshold as the C++ side
        "hue"_a, "luminosity"_a, "threshold"_a = 0.4,
        // the docstring
        "make a color from an {hl} pair");
    // from {oklch}
    rgb.def(
        // the name
        "oklch",
        // the converter
        &pyre::chroma::rgb::oklch,
        // the signature
        "lightness"_a, "chroma"_a, "hue"_a,
        // the docstring
        "make a color from an {oklch} triplet");

    // the color palette lives in a {palette} sub-submodule
    auto palette = rgb.def_submodule(
        // the name of the module
        "palette",
        // its docstring
        "the table of canonical color names");
    // look up a color by name
    palette.def(
        // the name
        "find",
        // the lookup
        &pyre::chroma::rgb::palette::find,
        // the signature
        "name"_a,
        // the docstring
        "look up a color by name; {None} when it is not in the table");

    // all done
    return;
}


// end of file
