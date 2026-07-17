// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// add a type to the beginning an existing list

// forward declaration
#include "forward.h"

// support
#include "types.h"


// prepend a type {T} to an existing {typesT} list
template <typename... typesT, typename... T>
struct pyre::typelists::prepend_t<pyre::typelists::types_t<typesT...>, T...> {
    // by making a new list
    using type = types_t<T..., typesT...>;
};


// end of file
