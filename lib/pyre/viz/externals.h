// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <algorithm>
#include <cassert>
#include <cmath>
#include <complex>
#include <cstdint>
#include <fstream>
#include <memory>
#include <tuple>
#include <type_traits>

// support
#include <pyre/journal.h>
#include <pyre/chroma.h>
#include <pyre/memory.h>
#include <pyre/grid.h>
#include <pyre/flow.h>


// the basic types, so we are on the same page as the packages they come from
namespace pyre::viz {
    // an interval is a pair of doubles, its two ends
    using interval_t = std::tuple<double, double>;
    // color channels and {r,g,b} triplets come from {chroma}, the single source of color truth
    using color_t = chroma::color_t;
    using rgb_t = chroma::rgb_t;
    // just to make sure we are all on the same page, wherever it matters
    using byte_t = unsigned char;
} // namespace pyre::viz


// end of file
