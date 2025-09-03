// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// support
#include "externals.h"


// low level entities; you should probably stay away from them
namespace pyre::grid {
    // packing order
    template <std::size_t Rank>
    using order_t = Order<Rank>;
    // shape
    template <std::size_t Rank>
    using shape_t = Shape<Rank>;

    // the grid
    template <class packingT, class storageT>
    using grid_t = Grid<packingT, storageT>;
} // namespace pyre::grid


// end of file
