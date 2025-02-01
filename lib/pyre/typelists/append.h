// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// add a type to the end of an existing list

// forward declaration
#include "forward.h"

// support
#include "types.h"


// append the types {T} to an existing {typesT} list
template <typename... typesT, typename... T>
struct pyre::typelists::append_t<pyre::typelists::types_t<typesT...>, T...> {
    // by making a new list
    using type = types_t<typesT..., T...>;
};


// end of file
