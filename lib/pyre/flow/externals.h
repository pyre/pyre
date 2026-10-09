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
    // the value of a setting of a factory, whatever its type
    using setting_t = std::variant<int, double, interval_t>;
} // namespace pyre::flow


// end of file
