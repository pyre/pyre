// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// forward declaration
#include "forward.h"


// a value container; the {auto} pack lets a single list hold values of mixed type,
// so both {values_t<true, false>} and {values_t<1, 2, 3, 4>} are well formed
template <auto...>
struct pyre::typelists::values_t {};


// end of file
