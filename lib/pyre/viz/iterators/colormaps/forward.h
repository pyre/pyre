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
namespace pyre::viz::iterators::colormaps {
    template <class sourceT>
    class Complex;
    template <class sourceT>
    class Gray;
    template <class hueSourceT, class luminositySourceT>
    class HL;
    template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
    class HSB;
    template <class hueSourceT, class saturationSourceT, class luminositySourceT>
    class HSL;
    template <class lightnessSourceT, class chromaSourceT, class hueSourceT>
    class OKLCH;
    template <class redSourceT, class greenSourceT, class blueSourceT>
    class RGB;
} // namespace pyre::viz::iterators::colormaps


// end of file
