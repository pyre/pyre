// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_public_h)
#define pyre_viz_public_h


// external packages
#include "external.h"
// set up the namespace
#include "forward.h"

// published type aliases and declarations that constitute the public API of this package
// this is the file you are looking for
#include "api.h"

// local support
// filters
#include "filters/Amplitude.h"
#include "filters/Constant.h"
#include "filters/Phase.h"
// color spaces
#include "colorspaces/hsb.h"
#include "colorspaces/hsl.h"
// color maps
#include "colormaps/Complex.h"
#include "colormaps/Gray.h"
#include "colormaps/HSB.h"
#include "colormaps/HSL.h"
#include "colormaps/RGB.h"
// encodings
#include "codecs/BMP.h"


#endif

// end of file
