// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// a helper that merges type lists

// forward declarations
#include "forward.h"

// support
#include "types.h"


// type U type
template <typename T, typename U>
struct pyre::typelists::merge_t<T, U> {
    using type = types_t<T, U>;
};

// nil U nil
template <>
struct pyre::typelists::merge_t<pyre::typelists::types_t<>, pyre::typelists::types_t<>> {
    using type = types_t<>;
};

// nil U list
template <typename carT, typename... cdrT>
struct pyre::typelists::merge_t<
    pyre::typelists::types_t<>, pyre::typelists::types_t<carT, cdrT...>> {
    using type = types_t<carT, cdrT...>;
};

// list U nil
template <typename carT, typename... cdrT>
struct pyre::typelists::merge_t<
    pyre::typelists::types_t<carT, cdrT...>, pyre::typelists::types_t<>> {
    using type = types_t<carT, cdrT...>;
};

// type U list
template <typename T, typename carT, typename... cdrT>
struct pyre::typelists::merge_t<T, pyre::typelists::types_t<carT, cdrT...>> {
    using type = types_t<T, carT, cdrT...>;
};


// end of file
