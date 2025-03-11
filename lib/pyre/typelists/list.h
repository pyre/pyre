// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include <utility>
// forward declarations
#include "forward.h"

// support
#include "types.h"


// a typelist with {N} copies of the given type {T}
template <typename T, int N, int... I>
struct pyre::typelists::list_t<T, N, std::index_sequence<I...>> {
    // put {N} copies of {T} in a typelists
    using type = types_t<typename type_t<T, I>::type...>;
};


// end of file
