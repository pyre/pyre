// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// STL
#include <algorithm>
#include <cmath>
#include <complex>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <tuple>
#include <type_traits>
#include <vector>

// support
#include <pyre/journal.h>
#include <pyre/grid.h>

// aliases
namespace pyre::flow {
    // strings
    using string_t = std::string;
    // an interval is a pair of doubles, its two ends
    using interval_t = std::tuple<double, double>;
} // namespace pyre::flow


// end of file
