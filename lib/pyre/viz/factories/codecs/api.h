// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::viz::factories::codecs}
#include "forward.h"


// factories
// codecs
namespace pyre::viz::factories::codecs {
    // microsoft bitmaps
    template <class redT, class greenT = redT, class blueT = redT>
    using bmp_t = BMP<redT, greenT, blueT>;
} // namespace pyre::viz::factories::codecs


// end of file
