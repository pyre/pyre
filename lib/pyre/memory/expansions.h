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


// expansion helpers
namespace pyre::memory {
    // the cell expander
    template <typename...>
    struct celltypes_t;
    // build a typelist with both const and mutable cells from a pile of basic types
    template <typename... T>
    struct celltypes_t<pyre::typelists::types_t<T...>> {
        using type = typename pyre::typelists::concat_t<
            pyre::typelists::types_t<cell_t<T, false>...>,
            pyre::typelists::types_t<cell_t<T, true>...>>::type;
    };

    // the storage strategy expander
    template <typename...>
    struct storageCells_t;
    // build a typelist of storage template expansion arguments suitable for handing off
    // to {pyre::typelists::apply_t}
    template <typename... T>
    struct storageCells_t<pyre::typelists::types_t<T...>> {
        using type = pyre::typelists::types_t<pyre::typelists::types_t<T>...>;
    };
} // namespace pyre::memory


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

    // the pile of cell types
    using cells_t = typename celltypes_t<basetypes_t>::type;

    // base buffers
    using buffers_t = typename pyre::typelists::apply_t<
        // the heaps
        pyre::typelists::templates_t<buffer_t, constbuffer_t>,
        // the cells
        typename storageCells_t<basetypes_t>::type>::type;

    // heaps over all base types
    using heaps_t = typename pyre::typelists::apply_t<
        // the heaps
        pyre::typelists::templates_t<heap_t, constheap_t>,
        // the cells
        typename storageCells_t<basetypes_t>::type>::type;

    // maps over all base types
    using maps_t = typename pyre::typelists::apply_t<
        // the heaps
        pyre::typelists::templates_t<map_t, constmap_t>,
        // the cells
        typename storageCells_t<basetypes_t>::type>::type;

    // views over all base types
    using views_t = typename pyre::typelists::apply_t<
        // the heaps
        pyre::typelists::templates_t<view_t, constview_t>,
        // the cells
        typename storageCells_t<basetypes_t>::type>::type;
} // namespace pyre::memory


// end of file
