// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

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
    // the const/mutable axis, expressed as a value list so it rides through the type algebra
    using constness_t = pyre::typelists::values_t<false, true>;

    // adapter that turns a (constness, base type) pair into the matching cell type; it exists so
    // the {cell_t} bool parameter can travel through the type-only {apply_t}/{cartesian_t}
    // machinery
    template <typename isConstT, typename T>
    using cellexp_t = cell_t<T, isConstT::value>;

    // the cell expander
    template <typename...>
    struct celltypes_t;
    // build a typelist with both mutable and const cells from a pile of basic types
    template <typename... T>
    struct celltypes_t<pyre::typelists::types_t<T...>> {
        // multiply the constness axis against the base types and stamp out a cell for each pair;
        // {cartesian_t} visits {false} across all bases before {true}, so mutable cells come first
        using type = typename pyre::typelists::apply_t<
            // the adapter as the sole template
            pyre::typelists::templates_t<cellexp_t>,
            // over the cartesian product of the lifted constness axis and the base types
            typename pyre::typelists::cartesian_t<
                typename pyre::typelists::lift_t<constness_t>::type,
                pyre::typelists::types_t<T...>>::type>::type;
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
