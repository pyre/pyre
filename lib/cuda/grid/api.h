// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// user facing types
namespace pyre::cuda::grid {
    // a grid over cuda managed memory, which the host and the device both reach
    template <class packingT, class cellT>
    using managed_t = pyre::grid::grid_t<packingT, pyre::cuda::memory::managed_t<cellT>>;

    // a grid over pinned host memory
    template <class packingT, class cellT>
    using pinned_t = pyre::grid::grid_t<packingT, pyre::cuda::memory::pinned_t<cellT>>;

    // a grid over host memory mapped into the address space of the device
    template <class packingT, class cellT>
    using mapped_t = pyre::grid::grid_t<packingT, pyre::cuda::memory::mapped_t<cellT>>;

    // a grid over the cells of another, without owning them; it copies trivially, so it is what
    // a kernel takes
    template <class packingT, class cellT>
    using view_t = pyre::grid::grid_t<packingT, pyre::memory::view_t<cellT>>;

    // a read only view
    template <class packingT, class cellT>
    using constview_t = pyre::grid::grid_t<packingT, pyre::memory::constview_t<cellT>>;
} // namespace pyre::cuda::grid


// end of file
