// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// get the common ones
#include "../external.h"
// the flow library
#include <pyre/flow.h>
// the type-erased grid, which is how python sees the cells of a tile
#include <pyre/py/grid/AnyGrid.h>


// aliases
namespace pyre::py::flow {
    // the protocols
    using node_t = pyre::flow::node_t;
    using product_t = pyre::flow::product_t;
    using factory_t = pyre::flow::factory_t;
    // the descriptions of the slots and the settings of factories
    using slot_t = pyre::flow::protocols::Slot;
    using setting_t = pyre::flow::protocols::Setting;
    // the catalog and its entries
    using catalog_t = pyre::flow::catalog::catalog_t;
    using product_entry_t = pyre::flow::catalog::ProductEntry;
    using factory_entry_t = pyre::flow::catalog::FactoryEntry;
    // all tiles are two dimensional, packed canonically
    using packing_t = pyre::grid::canonical_t<2>;
    // a tile over cells of type {cellT} on the heap
    template <typename cellT>
    using tile_t =
        pyre::flow::products::tile_t<pyre::grid::grid_t<packing_t, pyre::memory::heap_t<cellT>>>;
    // the type-erased grid
    using anygrid_t = pyre::py::grid::AnyGrid;
} // namespace pyre::py::flow


// end of file
