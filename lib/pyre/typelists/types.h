// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// forward declaration
#include "forward.h"


// a type container
template <typename...>
struct pyre::typelists::types_t {};

// type declarator
template <typename T, int>
struct pyre::typelists::type_t {
    // declare the type
    using type = T;
};


// end of file
