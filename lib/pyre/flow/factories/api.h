// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// factories
namespace pyre::flow::factories {
    // addition
    // atoms
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using add_variables_t = Add<products::Variable, op1T, op2T, resultT>;
    // tiles
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using add_tiles_t = Add<products::Tile, op1T, op2T, resultT>;

    // multiplication
    // atoms
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using multiply_variables_t = Multiply<products::Variable, op1T, op2T, resultT>;
    // tiles
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using multiply_tiles_t = Multiply<products::Tile, op1T, op2T, resultT>;
} // namespace pyre::flow::factories


// end of file
