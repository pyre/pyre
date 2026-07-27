// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

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
    // diagonal packing strategy
    template <std::size_t Rank>
    using diagonal_t = Diagonal<Rank>;
    // symmetric packing strategy
    template <std::size_t Rank>
    using symmetric_t = Symmetric<Rank>;
    // chunked packing strategy
    template <std::size_t Rank>
    using chunked_t = Chunked<Rank>;
    // dynamic (runtime-rank) variants
    using dynamic_index_iterator_t = DynamicIndexIterator;
    using dynamic_canonical_t = DynamicCanonical;

    // the grid
    template <class packingT, class storageT>
    using grid_t = Grid<packingT, storageT>;
    // and the cursor that walks its cells
    template <class gridT>
    using grid_iterator_t = GridIterator<gridT>;

    // the mosaic: a chunked packing married to paged storage, the out-of-core grid whose tiles
    // materialize on demand and travel as zero-copy panes
    template <std::size_t Rank, typename T>
    using mosaic_t = Grid<Chunked<Rank>, pyre::memory::paged_t<T>>;
    // read-only version
    template <std::size_t Rank, typename T>
    using constmosaic_t = Grid<Chunked<Rank>, pyre::memory::constpaged_t<T>>;
} // namespace pyre::grid


// end of file
