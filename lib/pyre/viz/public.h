// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

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
// images
#include "products/images/BMP.h"

// factories
// codecs
#include "factories/codecs/BMP.h"
// color maps
#include "factories/colormaps/Complex.h"
#include "factories/colormaps/Gray.h"
#include "factories/colormaps/HL.h"
#include "factories/colormaps/HSB.h"
#include "factories/colormaps/HSL.h"
// filters
#include "factories/filters/Affine.h"
#include "factories/filters/Constant.h"
#include "factories/filters/Cycle.h"
#include "factories/filters/Decimate.h"
#include "factories/filters/Geometric.h"
#include "factories/filters/LogSaw.h"
#include "factories/filters/Parametric.h"
#include "factories/filters/PolarSaw.h"
#include "factories/filters/Power.h"
#include "factories/filters/Uniform.h"
// selectors
#include "factories/selectors/Amplitude.h"
#include "factories/selectors/Imaginary.h"
#include "factories/selectors/Phase.h"
#include "factories/selectors/Real.h"

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
