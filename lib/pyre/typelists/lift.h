// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// raise a value list into a type list so the type algebra can operate on it

// forward declarations
#include "forward.h"

// support
#include "types.h"
#include "values.h"

// STL
#include <type_traits>


// lift every value {vT} into an {std::integral_constant} of its own type; the result is an
// ordinary {types_t}, so {concat_t}, {cartesian_t}, {apply_t}, ... all work on it unchanged
template <auto... vT>
struct pyre::typelists::lift_t<pyre::typelists::values_t<vT...>> {
    // wrap each value in a compile-time constant carrying both its type and its value
    using type = types_t<std::integral_constant<decltype(vT), vT>...>;
};


// end of file
