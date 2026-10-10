// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the factories of {pyre::viz} this extension was compiled with; python reaches them through
// the {Factory} protocol, so they go in the catalog rather than get classes of their own
void
pyre::py::viz::factories(py::module &)
{
    // the tiles
    using float32_t = pyre::py::flow::tile_t<pyre::memory::float32_t>;
    using float64_t = pyre::py::flow::tile_t<pyre::memory::float64_t>;

    // get the catalog
    auto & catalog = pyre::py::flow::registry();
    // colormaps
    // gray, in single precision, for the channels that paint a value
    catalog.registerFactory<pyre::viz::factories::colormaps::gray_t<float32_t>>();
    // the colormaps make colors in single precision, the way the iterators do, so the encoder
    // scales them to bytes with the same rounding
    // hue, saturation, and brightness, in double precision, for the phase
    catalog.registerFactory<pyre::viz::factories::colormaps::hsb_t<
        float64_t, float64_t, float64_t, float32_t, float32_t, float32_t>>();
    // and with a single precision brightness, for the complex channel
    catalog.registerFactory<pyre::viz::factories::colormaps::hsb_t<
        float64_t, float64_t, float32_t, float32_t, float32_t, float32_t>>();
    // hue and luminosity, in double precision, for the phase and the complex values of
    // interferograms
    catalog.registerFactory<pyre::viz::factories::colormaps::hl_t<
        float64_t, float64_t, float32_t, float32_t, float32_t>>();
    // codecs
    // the bitmap of single precision colors
    catalog.registerFactory<pyre::viz::factories::codecs::bmp_t<float32_t>>();
    // and of double precision ones
    catalog.registerFactory<pyre::viz::factories::codecs::bmp_t<float64_t>>();

    // all done
    return;
}


// end of file
