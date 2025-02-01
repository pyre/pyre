// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// join type lists

// forward declarations
#include "forward.h"

// support
#include "types.h"


// base case: no arguments -> empty list
template <>
struct pyre::typelists::concat_t<> {
    using type = types_t<>;
};

// base case: one argument is returned as it
template <typename... T>
struct pyre::typelists::concat_t<pyre::typelists::types_t<T...>> {
    using type = types_t<T...>;
};

// base case: concatenate two lists
template <typename... l1T, typename... l2T>
struct pyre::typelists::concat_t<
    pyre::typelists::types_t<l1T...>, pyre::typelists::types_t<l2T...>> {
    using type = types_t<l1T..., l2T...>;
};

// the recursive case for n lists
template <typename l1T, typename l2T, typename... restT>
struct pyre::typelists::concat_t<l1T, l2T, restT...> {
    using type = typename concat_t<typename concat_t<l1T, l2T>::type, restT...>::type;
};


// end of file
