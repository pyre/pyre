// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// external
#include "externals.h"
// forward declaration
#include "forward.h"
// the api
#include "api.h"


// low level entities; you should probably stay away from them
namespace pyre::memory {
    // access rights
    using const_t = std::integer_sequence<bool, true, false>;
    // cell types
    using basetypes_t = pyre::typelists::types_t<
        // signed integers
        int8_t, int16_t, int32_t, int64_t,
        // unsigned integers
        uint8_t, uint16_t, uint32_t, uint64_t,
        // floating point
        float32_t, float64_t,
        // complex
        complex64_t, complex128_t>;

    // the cell expander
    template <typename... baseT>
    struct celltypes_t<pyre::typelists::types_t<baseT...>> {
        using type = typename pyre::typelists::concat_t<
            pyre::typelists::types_t<cell_t<baseT, false>...>,
            pyre::typelists::types_t<cell_t<baseT, true>...>>::type;
    };

    // the pile of cell types
    using cells_t = typename celltypes_t<basetypes_t>::type;

    // storage strategies by category
    using heaps_t = pyre::typelists::templates_t<constheap_t, heap_t>;
    using maps_t = pyre::typelists::templates_t<constmap_t, map_t>;
    using views_t = pyre::typelists::templates_t<constview_t, view_t>;

    // all storage strategies
    using storageStrategies =
        pyre::typelists::templates_t<constheap_t, constmap_t, constview_t, heap_t, map_t, view_t>;
} // namespace pyre::memory


// end of file
