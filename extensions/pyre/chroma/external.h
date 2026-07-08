// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// get the common bindings support
#include "../external.h"
// pybind11 operator helpers, for binding {==}
#include <pybind11/operators.h>
// get the chroma library: the color type, the {rgb} converters, and the {ansi} serializers
#include <pyre/chroma.h>


// aliases
namespace pyre::py::chroma {
    // the canonical color type
    using rgb_t = pyre::chroma::rgb_t;
    // a single color channel
    using color_t = pyre::chroma::color_t;
} // namespace pyre::py::chroma


// end of file
