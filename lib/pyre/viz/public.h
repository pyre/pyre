// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

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
// color spaces
#include "colorspaces/hl.h"
#include "colorspaces/hsb.h"
#include "colorspaces/hsl.h"

// products
// memory
#include "products/memory/I1.h"
// images
#include "products/images/BMP.h"

// iterators
// filters
#include "iterators/filters/Add.h"
#include "iterators/filters/Affine.h"
#include "iterators/filters/Amplitude.h"
#include "iterators/filters/Constant.h"
#include "iterators/filters/Cycle.h"
#include "iterators/filters/Decimate.h"
#include "iterators/filters/Geometric.h"
#include "iterators/filters/Imaginary.h"
#include "iterators/filters/LogSaw.h"
#include "iterators/filters/Multiply.h"
#include "iterators/filters/Parametric.h"
#include "iterators/filters/Phase.h"
#include "iterators/filters/PolarSaw.h"
#include "iterators/filters/Power.h"
#include "iterators/filters/Real.h"
#include "iterators/filters/Uniform.h"
// color maps
#include "iterators/colormaps/Complex.h"
#include "iterators/colormaps/Gray.h"
#include "iterators/colormaps/HL.h"
#include "iterators/colormaps/HSB.h"
#include "iterators/colormaps/HSL.h"
#include "iterators/colormaps/RGB.h"
// encodings
#include "iterators/codecs/BMP.h"


#endif

// end of file
