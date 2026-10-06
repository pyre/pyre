// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// colorspaces
namespace pyre::viz::factories::colormaps {
    // grayscale
    template <class signalT, class redT = signalT, class greenT = redT, class blueT = redT>
    using gray_t = Gray<signalT, redT, greenT, blueT>;

    // hue based spaces
    template <
        class hueT, class luminosityT = hueT, class redT = hueT, class greenT = hueT,
        class blueT = hueT>
    using hl_t = HL<hueT, luminosityT, redT, greenT, blueT>;

    template <
        class hueT, class saturationT = hueT, class brightnessT = hueT, class redT = hueT,
        class greenT = hueT, class blueT = hueT>
    using hsb_t = HSB<hueT, saturationT, brightnessT, redT, greenT, blueT>;

    template <
        class hueT, class saturationT = hueT, class luminosityT = hueT, class redT = hueT,
        class greenT = hueT, class blueT = hueT>
    using hsl_t = HSL<hueT, saturationT, luminosityT, redT, greenT, blueT>;

    // complex data
    template <class signalT, class redT, class greenT = redT, class blueT = redT>
    using complex_t = Complex<signalT, redT, greenT, blueT>;
} // namespace pyre::viz::factories::colormaps


// end of file
