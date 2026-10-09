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
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <set>
#include <string>
#include <tuple>
#include <type_traits>
#include <variant>
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
    // a pair of integers, one per axis of a tile, such as an origin or a stride
    using pair_t = std::tuple<int, int>;
    // the value of a setting of a factory, whatever its type; a pair comes before an interval, so
    // a pair of integers from python lands on it, and an interval takes it by widening
    using setting_t = std::variant<int, double, pair_t, interval_t>;
} // namespace pyre::flow


// end of file
