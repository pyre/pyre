// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::flow::products}
#include "forward.h"


// products
namespace pyre::flow::products {
    // atoms
    template <typename valueT>
    using var_t = Variable<valueT>;
    // tiles
    template <class gridT>
    using tile_t = Tile<gridT>;
} // namespace pyre::flow::products


// end of file
