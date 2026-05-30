// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// support
#include "externals.h"
// forward declarations
#include "forward.h"


// low level entities; you should probably stay away from them
namespace pyre::grid {
    // packing order
    template <std::size_t Rank>
    using order_t = Order<Rank>;
    // shape
    template <std::size_t Rank>
    using shape_t = Shape<Rank>;
    // index
    template <std::size_t Rank>
    using index_t = Index<Rank>;
    // index iterator
    template <std::size_t Rank>
    using index_iterator_t = IndexIterator<Rank>;
    // canonical packing strategy
    template <std::size_t Rank>
    using canonical_t = Canonical<Rank>;
    // dynamic (runtime-rank) variants
    using dynamic_index_iterator_t = DynamicIndexIterator;
    using dynamic_canonical_t = DynamicCanonical;

    // the grid
    template <class packingT, class storageT>
    using grid_t = Grid<packingT, storageT>;
} // namespace pyre::grid


// end of file
