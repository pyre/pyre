// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include <tuple>
// forward declarations
#include "forward.h"

// support
#include "types.h"

// conversion of a type list to a tuple
template <typename... T>
struct pyre::typelists::tuple_t<pyre::typelists::types_t<T...>> {
    using type = std::tuple<T...>;
};


// end of file
