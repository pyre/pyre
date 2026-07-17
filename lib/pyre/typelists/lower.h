// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// bring a type list of compile-time constants back down to a value list

// forward declarations
#include "forward.h"

// support
#include "types.h"
#include "values.h"


// read the {::value} out of every constant in the {cT} list and collect them into a value list;
// this is the inverse of {lift_t}, so {lower_t<lift_t<L>::type>::type} recovers the original {L}
template <typename... cT>
struct pyre::typelists::lower_t<pyre::typelists::types_t<cT...>> {
    // pull the stored value from each constant
    using type = values_t<cT::value...>;
};


// end of file
