// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "../../forward.h"


// forward declarations
namespace pyre::viz::factories::colormaps {
    // grayscale
    template <class signalT, class redT, class greenT, class blueT>
    class Gray;
    // hue based spaces
    template <class hueT, class luminosityT, class redT, class greenT, class blueT>
    class HL;
    template <
        class hueT, class saturationT, class brightnessT, class redT, class greenT,
        class blueT>
    class HSB;
    template <
        class hueT, class saturationT, class luminosityT, class redT, class greenT,
        class blueT>
    class HSL;
    // a factory for complex inputs
    template <class signalT, class redT, class greenT, class blueT>
    class Complex;
} // namespace pyre::viz::factories::colormaps


// end of file
