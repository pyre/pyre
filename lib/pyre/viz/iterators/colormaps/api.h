// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::viz::iterators::colormaps}
#include "forward.h"


// color maps
namespace pyre::viz::iterators::colormaps {
    template <class sourceT>
    using complex_t = Complex<sourceT>;

    template <class sourceT>
    using gray_t = Gray<sourceT>;

    template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
    using hsb_t = HSB<hueSourceT, saturationSourceT, brightnessSourceT>;

    template <class hueSourceT, class luminositySourceT>
    using hl_t = HL<hueSourceT, luminositySourceT>;

    template <class hueSourceT, class saturationSourceT, class luminositySourceT>
    using hsl_t = HSL<hueSourceT, saturationSourceT, luminositySourceT>;

    template <class lightnessSourceT, class chromaSourceT, class hueSourceT>
    using oklch_t = OKLCH<lightnessSourceT, chromaSourceT, hueSourceT>;

    template <class redSourceT, class greenSourceT, class blueSourceT>
    using rgb_t = RGB<redSourceT, greenSourceT, blueSourceT>;
} // namespace pyre::viz::iterators::colormaps


// end of file
