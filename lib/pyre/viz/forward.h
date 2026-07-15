// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "external.h"


// set up the namespace and its shared aliases
namespace pyre::viz {
    // an interval is a pair of
    using interval_t = std::tuple<double, double>;
    // color channels and {r,g,b} triplets come from {chroma}, the single source of color truth
    using color_t = chroma::color_t;
    using rgb_t = chroma::rgb_t;
    // just to make sure we are all on the same page, wherever it matters
    using byte_t = unsigned char;
    // aliases for the atomic types
    // signed integers
    using i1_t = std::int8_t;
    using i2_t = std::int16_t;
    using i4_t = std::int32_t;
    using i8_t = std::int64_t;
    // unsigned integers
    using u1_t = std::uint8_t;
    using u2_t = std::uint16_t;
    using u4_t = std::uint32_t;
    using u8_t = std::uint64_t;
    // floats
    using f4_t = float;
    using f8_t = double;
    // complex
    using c8_t = std::complex<float>;
    using c16_t = std::complex<double>;
    // products
} // namespace pyre::viz


// the per-namespace forward declarations
#include "products/forward.h"
#include "factories/forward.h"
#include "iterators/forward.h"


// end of file
